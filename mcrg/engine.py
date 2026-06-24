from __future__ import annotations

import itertools

from .loaders import cargar_dataframe_with_report
from .smiles_utils import parse_smiles_flexible


def run_mcr(
    mcr_key,
    file_paths,
    catalog,
    core_smiles_list=None,
    threshold=50.0,
    progress_cb=None,
    standardize=True,
    ideal_rule="Lipinski",
    *,
    pd,
    Chem,
    AllChem,
    Descriptors,
    Lipinski,
    _CHEM_READY: bool,
):
    """
    Core MCR engine. Kept free of GUI dependencies.

    The GUI entrypoint (`mcrg_desktop.py`) injects heavy deps (RDKit/pandas).
    """
    info = catalog[mcr_key]
    comps = info["componentes"]
    listas, preview = [], []
    # NOTE: "Total evaluated" counts *all* attempted combinations, including failures (no product).
    # The UI expects:
    # - Ideal: all successful product generations
    # - Discarded: all failed attempts
    # - All: every attempt (Ideal + Discarded) == Total evaluated
    # Include component names + SMILES + failure reason so Discarded rows are explainable in the UI.
    comp_smiles_cols = [f"{c}_SMILES" for c in comps]
    cols = [
        "Compatibility_%",
        # Chirality / stereochemistry (derived from SMILES_Final)
        "Chiral_Centers",
        "Chiral_Centers_Defined",
        "Chiral_Centers_Unassigned",
        "Chiral_Tags",
        "Has_Stereo",
        "Molecular_Weight",
        "LogP",
        "TPSA",
        "HBA",
        "HBD",
        "QED",
        "Fsp3",
        "PAINS_Alerts",
        "Brenk_Alerts",
        "Rotatable_Bonds",
        "Heavy_Atoms",
        "Ring_Count",
        "Molar_Refractivity",
        "Pass_Lipinski",
        "Pass_Ghose",
        "Pass_Veber",
        "Pass_Egan",
        "Pass_Muegge",
        "Ideal_Rule",
        "SMILES_Final",
        "InChIKey",
        "Is_Duplicate",
        "Duplicate_Of",
        "Classification",
        "Review_Status",
        "Core_Reagent",
        "Failure_Reason",
    ] + comps + comp_smiles_cols
    empty_df = pd.DataFrame(columns=cols)

    # core_smiles_list can be:
    # - list[str] (SMILES)
    # - list[tuple[name, smiles]]
    core_mols = []
    if core_smiles_list and _CHEM_READY:
        for item in core_smiles_list:
            if isinstance(item, (tuple, list)) and len(item) >= 2:
                core_name, smi = str(item[0]), str(item[1])
            else:
                core_name, smi = str(item), str(item)
            mol = parse_smiles_flexible(smi, Chem)
            if mol:
                try:
                    Chem.SanitizeMol(mol)
                    core_mols.append((core_name, smi, mol))
                except Exception:
                    continue

    for i, fp in enumerate(file_paths):
        try:
            df, rep, rej = cargar_dataframe_with_report(fp, pd=pd, validate_rdkit=True, Chem=Chem, _CHEM_READY=_CHEM_READY)
            listas.append(list(zip(df["NAME"], df["SMILES"])))
            # Input QC summary (prevents silent data loss confusion)
            try:
                qc = f"{rep.get('rows_valid', len(df))}/{rep.get('rows_raw', len(df))}"
                extra = []
                if rep.get("rows_invalid_smiles", 0):
                    extra.append(f"invalid_smiles={int(rep.get('rows_invalid_smiles', 0))}")
                if int(rep.get("rows_raw", 0)) - int(rep.get("rows_nonempty_smiles", 0)) > 0:
                    extra.append(f"empty_smiles={int(rep.get('rows_raw', 0)) - int(rep.get('rows_nonempty_smiles', 0))}")
                extra_txt = (" | " + ", ".join(extra)) if extra else ""
                preview.append(f"— {comps[i]}: {qc} valid rows{extra_txt} —")
            except Exception:
                preview.append(f"— {comps[i]}: {len(df)} valid records —")
            try:
                if "_input_qc" not in locals():
                    _input_qc = {"components": [], "rejected_rows": {}}
                _input_qc["components"].append(rep)
                if rej is not None and not getattr(rej, "empty", True):
                    _input_qc["rejected_rows"][comps[i]] = int(len(rej))
            except Exception:
                pass
        except Exception as e:
            preview.append(f"❌ Error loading {comps[i]}: {e}")
            return empty_df, empty_df, "\n".join(preview)

    if not all(listas):
        preview.append("⚠ One or more files are empty or invalid.")
        return empty_df, empty_df, "\n".join(preview)

    rxn = AllChem.ReactionFromSmarts(info["smarts"])
    if not rxn:
        preview.append("❌ Invalid reaction SMARTS.")
        return empty_df, empty_df, "\n".join(preview)
    rxn_variants = [rxn]
    for extra_smarts in info.get("smarts_variants", []) or []:
        try:
            extra_rxn = AllChem.ReactionFromSmarts(extra_smarts)
        except Exception:
            extra_rxn = None
        if extra_rxn:
            rxn_variants.append(extra_rxn)

    def _mol_matches_template(mol, template) -> bool:
        try:
            return bool(mol is not None and template is not None and mol.HasSubstructMatch(template))
        except Exception:
            return False

    def _preflight_template_summary(insert_idx=None):
        rows = []
        if not _CHEM_READY:
            return rows
        for comp_i, comp in enumerate(comps):
            lst = listas[comp_i] if comp_i < len(listas) else []
            if not lst:
                continue
            matched = 0
            unmatched = []
            for name, smi in lst:
                mol = parse_smiles_flexible(smi, Chem)
                if not mol or not _safe_sanitize(mol):
                    unmatched.append(str(name))
                    continue
                ok = False
                for rxn_obj in rxn_variants:
                    try:
                        n_templates = int(rxn_obj.GetNumReactantTemplates())
                    except Exception:
                        continue
                    if insert_idx is None:
                        template_idx = comp_i
                        expected = len(comps)
                    else:
                        template_idx = comp_i + (1 if comp_i >= int(insert_idx) else 0)
                        expected = len(comps) + 1
                    if n_templates != expected or template_idx >= n_templates:
                        continue
                    try:
                        tmpl = rxn_obj.GetReactantTemplate(template_idx)
                    except Exception:
                        tmpl = None
                    if _mol_matches_template(mol, tmpl):
                        ok = True
                        break
                if ok:
                    matched += 1
                else:
                    unmatched.append(str(name))
            rows.append(
                {
                    "component": comp,
                    "matched": int(matched),
                    "total": int(len(lst)),
                    "unmatched_examples": unmatched[:3],
                }
            )
        return rows

    def _append_preflight_to_preview(rows):
        if not rows:
            return
        preview.append("🔎 Reaction preflight:")
        for r in rows:
            total = int(r.get("total", 0))
            matched = int(r.get("matched", 0))
            comp = str(r.get("component", ""))
            msg = f"   - {comp}: {matched}/{total} rows match the reaction template"
            examples = [x for x in r.get("unmatched_examples", []) if x]
            if examples:
                msg += " | outside pattern: " + ", ".join(examples)
            preview.append(msg)

    def _safe_sanitize(m):
        try:
            Chem.SanitizeMol(m)
            return True
        except Exception:
            return False

    def _standardize_product(m):
        """
        Conservative standardization: cleanup + fragment parent + uncharge.
        Best-effort; if standardization fails, returns the original molecule.
        """
        if not standardize or not _CHEM_READY:
            return m

        try:
            from rdkit.Chem.MolStandardize import rdMolStandardize
        except Exception:
            return m
        try:
            mm = rdMolStandardize.Cleanup(m)
            try:
                mm = rdMolStandardize.FragmentParent(mm)
            except Exception:
                pass
            try:
                mm = rdMolStandardize.Uncharger().uncharge(mm)
            except Exception:
                pass
            try:
                Chem.SanitizeMol(mm)
            except Exception:
                pass
            return mm
        except Exception:
            return m

    def _druglikeness_metrics(prod_mol):
        """
        Compute descriptors + multiple rule-of-thumb filters (best-effort, deterministic).
        Returns a dict with descriptor fields + Pass_* booleans.
        """
        try:
            mw = float(Descriptors.MolWt(prod_mol))
            logp = float(Descriptors.MolLogP(prod_mol))
            tpsa = float(Descriptors.TPSA(prod_mol))
            hbd = int(Lipinski.NumHDonors(prod_mol))
            hba = int(Lipinski.NumHAcceptors(prod_mol))
            rb = int(Lipinski.NumRotatableBonds(prod_mol))
            heavy = int(prod_mol.GetNumHeavyAtoms())
            rings = int(Lipinski.RingCount(prod_mol))
            mr = float(Descriptors.MolMR(prod_mol))
        except Exception:
            return None

        # Lipinski (Ro5)
        pass_lipinski = (mw <= 500 and logp <= 5 and hbd <= 5 and hba <= 10)

        # Ghose (classic filter)
        # MW: 160–480, LogP: -0.4–5.6, MR: 40–130, atoms: 20–70
        pass_ghose = (160 <= mw <= 480 and -0.4 <= logp <= 5.6 and 40 <= mr <= 130 and 20 <= heavy <= 70)

        # Veber: RB <= 10 and (TPSA <= 140 or HBD+HBA <= 12)
        pass_veber = (rb <= 10 and (tpsa <= 140 or (hbd + hba) <= 12))

        # Egan: TPSA <= 131.6 and LogP <= 5.88
        pass_egan = (tpsa <= 131.6 and logp <= 5.88)

        # Muegge (Bayer): MW 200–600, LogP -2–5, TPSA <= 150, RB <= 15,
        # HBD <= 5, HBA <= 10, rings <= 7
        pass_muegge = (200 <= mw <= 600 and -2 <= logp <= 5 and tpsa <= 150 and rb <= 15 and hbd <= 5 and hba <= 10 and rings <= 7)

        # Additional presentation metrics (SwissADME-like sections, computed locally)
        try:
            from rdkit.Chem import rdMolDescriptors as _rdmd
            fsp3 = float(_rdmd.CalcFractionCSP3(prod_mol))
        except Exception:
            fsp3 = None
        try:
            from rdkit.Chem import QED as _QED
            qed = float(_QED.qed(prod_mol))
        except Exception:
            qed = None

        # MedChem structural alerts (best-effort)
        pains = 0
        brenk = 0
        try:
            from rdkit.Chem import FilterCatalog
            p = getattr(_druglikeness_metrics, "_pains", None)
            b = getattr(_druglikeness_metrics, "_brenk", None)
            if p is None:
                params = FilterCatalog.FilterCatalogParams()
                params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.PAINS)
                p = FilterCatalog.FilterCatalog(params)
                _druglikeness_metrics._pains = p
            if b is None:
                params = FilterCatalog.FilterCatalogParams()
                params.AddCatalog(FilterCatalog.FilterCatalogParams.FilterCatalogs.BRENK)
                b = FilterCatalog.FilterCatalog(params)
                _druglikeness_metrics._brenk = b
            pains = len(p.GetMatches(prod_mol)) if p else 0
            brenk = len(b.GetMatches(prod_mol)) if b else 0
        except Exception:
            pains = 0
            brenk = 0

        return {
            "Molecular_Weight": round(mw, 2),
            "LogP": round(logp, 2),
            "TPSA": round(tpsa, 2),
            "HBA": hba,
            "HBD": hbd,
            "Rotatable_Bonds": rb,
            "Heavy_Atoms": heavy,
            "Ring_Count": rings,
            "Molar_Refractivity": round(mr, 2),
            "QED": (round(qed, 3) if qed is not None else ""),
            "Fsp3": (round(fsp3, 3) if fsp3 is not None else ""),
            "PAINS_Alerts": int(pains),
            "Brenk_Alerts": int(brenk),
            "Pass_Lipinski": bool(pass_lipinski),
            "Pass_Ghose": bool(pass_ghose),
            "Pass_Veber": bool(pass_veber),
            "Pass_Egan": bool(pass_egan),
            "Pass_Muegge": bool(pass_muegge),
        }

    def _chirality_metrics(prod_mol):
        """
        Best-effort stereochemistry summary for UI/export.
        Deterministic and lightweight; does not enumerate stereoisomers.
        """
        try:
            # Ensure stereochemistry perception is up-to-date
            try:
                Chem.AssignStereochemistry(prod_mol, cleanIt=True, force=True)
            except Exception:
                pass

            centers = Chem.FindMolChiralCenters(prod_mol, includeUnassigned=True)
            n_total = int(len(centers))
            n_unassigned = int(sum(1 for _, tag in centers if str(tag) in ("?", "Unspecified")))
            n_defined = int(n_total - n_unassigned)
            tags = ",".join([f"{idx}:{tag}" for idx, tag in centers]) if centers else ""

            # Simple stereo presence heuristic: any chiral center or any E/Z bond flag in SMILES
            try:
                smi_iso = Chem.MolToSmiles(prod_mol, isomericSmiles=True)
            except Exception:
                smi_iso = ""
            has_stereo = bool(n_total > 0 or ("@" in smi_iso) or ("/" in smi_iso) or ("\\" in smi_iso))
            return {
                "Chiral_Centers": n_total,
                "Chiral_Centers_Defined": n_defined,
                "Chiral_Centers_Unassigned": n_unassigned,
                "Chiral_Tags": tags,
                "Has_Stereo": has_stereo,
            }
        except Exception:
            return {
                "Chiral_Centers": "",
                "Chiral_Centers_Defined": "",
                "Chiral_Centers_Unassigned": "",
                "Chiral_Tags": "",
                "Has_Stereo": "",
            }

    def _passes_selected_rule(metrics: dict) -> bool:
        k = str(ideal_rule or "Lipinski")
        if k == "Lipinski":
            return bool(metrics.get("Pass_Lipinski"))
        if k == "Ghose":
            return bool(metrics.get("Pass_Ghose"))
        if k == "Veber":
            return bool(metrics.get("Pass_Veber"))
        if k == "Egan":
            return bool(metrics.get("Pass_Egan"))
        if k == "Muegge":
            return bool(metrics.get("Pass_Muegge"))
        if k == "Any":
            return any(bool(metrics.get(x)) for x in ("Pass_Lipinski", "Pass_Ghose", "Pass_Veber", "Pass_Egan", "Pass_Muegge"))
        if k == "All":
            return all(bool(metrics.get(x)) for x in ("Pass_Lipinski", "Pass_Ghose", "Pass_Veber", "Pass_Egan", "Pass_Muegge"))
        return bool(metrics.get("Pass_Lipinski"))

    def _rule_fail_reason() -> str:
        k = str(ideal_rule or "Lipinski")
        if k in ("Any", "All"):
            return f"Fails rule set ({k})"
        return f"Fails {k} criteria"

    def _first_valid_mol_from_list(lst):
        for _, smi in lst:
            m = parse_smiles_flexible(smi, Chem)
            if m and _safe_sanitize(m):
                return m
        return None

    def _find_core_insert_index(rxn_objs, listas_local, core_mol_obj):
        if not isinstance(rxn_objs, (list, tuple)):
            rxn_objs = [rxn_objs]

        base_mols = []
        for lst in listas_local:
            m = _first_valid_mol_from_list(lst)
            if m is None:
                return 1
            base_mols.append(m)

        for rxn_obj in rxn_objs:
            try:
                if int(rxn_obj.GetNumReactantTemplates()) == len(base_mols):
                    return 1
            except Exception:
                continue

        for idx in range(0, len(base_mols) + 1):
            mols_try = base_mols.copy()
            mols_try.insert(idx, core_mol_obj)
            for rxn_obj in rxn_objs:
                try:
                    n_templates = int(rxn_obj.GetNumReactantTemplates())
                except Exception:
                    n_templates = None
                if n_templates is not None and len(mols_try) != n_templates:
                    continue
                try:
                    prods = rxn_obj.RunReactants(tuple(mols_try))
                    if prods:
                        return idx
                except Exception:
                    continue
        return 1

    def _first_sanitized_reaction_product(moles):
        """
        Try the primary reaction plus curated variants and return the first
        product RDKit can sanitize. This prevents valid combinations from being
        discarded when an earlier resonance/product candidate is not usable.
        """
        saw_products = False
        saw_sanitize_failure = False
        last_exception = ""
        for rxn_obj in rxn_variants:
            try:
                product_sets = rxn_obj.RunReactants(tuple(moles))
            except Exception as e:
                last_exception = str(e)[:140]
                continue
            if product_sets:
                saw_products = True
            for product_set in product_sets:
                if not product_set:
                    continue
                prod = _standardize_product(product_set[0])
                if _safe_sanitize(prod):
                    return prod, ""
                saw_sanitize_failure = True
        if saw_sanitize_failure:
            return None, "Product sanitize failed"
        if saw_products:
            return None, "Product sanitize failed"
        if last_exception:
            return None, f"Reaction execution failed: {last_exception}"
        return None, "No products generated by reaction SMARTS"

    def _run_summary(df_all_local, df_ideal_local):
        total = int(len(df_all_local)) if df_all_local is not None else 0
        if df_all_local is None or getattr(df_all_local, "empty", True):
            return {
                "evaluated": total,
                "products_valid": 0,
                "ideal_raw": 0,
                "ideal_unique": 0,
                "warning": 0,
                "error": 0,
                "discarded": 0,
                "reaction_failed": 0,
                "rule_failed": 0,
                "below_threshold": 0,
                "duplicates": 0,
                "failure_reasons": {},
                "hints": [],
            }
        try:
            cls = df_all_local["Classification"].astype(str) if "Classification" in df_all_local.columns else []
            ideal_raw = int((cls == "Ideal").sum()) if len(cls) else 0
        except Exception:
            ideal_raw = 0
        try:
            status = df_all_local["Review_Status"].fillna("").astype(str) if "Review_Status" in df_all_local.columns else []
            warning = int((status == "Warning").sum()) if len(status) else 0
            error = int((status == "Error").sum()) if len(status) else 0
        except Exception:
            warning = 0
            error = 0
        try:
            smiles = df_all_local["SMILES_Final"].fillna("").astype(str) if "SMILES_Final" in df_all_local.columns else []
            products_valid = int((smiles.str.len() > 0).sum()) if len(smiles) else 0
        except Exception:
            products_valid = 0
        try:
            reasons = df_all_local["Failure_Reason"].fillna("").astype(str) if "Failure_Reason" in df_all_local.columns else []
            failure_reasons = {str(k): int(v) for k, v in reasons.value_counts(dropna=False).items() if str(k)}
            below_threshold = int(reasons.str.startswith("Below threshold").sum()) if len(reasons) else 0
            rule_failed = int(reasons.str.startswith("Fails").sum()) if len(reasons) else 0
            sanitize_failed = int((reasons == "Product sanitize failed").sum()) if len(reasons) else 0
            no_products = int((reasons == "No products generated by reaction SMARTS").sum()) if len(reasons) else 0
        except Exception:
            failure_reasons = {}
            below_threshold = rule_failed = sanitize_failed = no_products = 0
        try:
            duplicates = int((df_all_local["Is_Duplicate"] == True).sum()) if "Is_Duplicate" in df_all_local.columns else 0
        except Exception:
            duplicates = 0

        discarded = int(total - ideal_raw)
        reaction_failed = int(max(0, total - products_valid))
        hints = []
        if total and ideal_raw == 0 and products_valid == 0:
            hints.append("No valid products were formed. Check whether each file contains reactants compatible with the selected reaction.")
        elif total and ideal_raw == 0 and products_valid > 0:
            hints.append("Products were formed, but filters classified all of them as Discarded. Try a lower threshold or a less strict Ideal criterion.")
        if below_threshold:
            hints.append("Some products are below the score threshold. Lower the threshold to inspect them in the Ideal view.")
        if rule_failed:
            hints.append(f"Some products fail the selected Ideal rule ({ideal_rule}). Switch to Any or another rule to compare.")
        if mcr_key == "GBB (3-CR)" and no_products:
            hints.append("GBB is sensitive to the aminoazine pattern. Aminoazines outside the supported 2-aminoazine core may not produce products.")
        if mcr_key == "Gewald (3-CR)" and sanitize_failed:
            hints.append("Gewald generated products for some combinations that RDKit could not sanitize; inspect alpha-substituted cyano partners first.")
        return {
            "evaluated": total,
            "products_valid": int(products_valid),
            "ideal_raw": int(ideal_raw),
            "ideal_unique": int(len(df_ideal_local)) if df_ideal_local is not None else 0,
            "warning": int(warning),
            "error": int(error),
            "discarded": discarded,
            "reaction_failed": reaction_failed,
            "rule_failed": int(rule_failed),
            "below_threshold": int(below_threshold),
            "duplicates": int(duplicates),
            "failure_reasons": failure_reasons,
            "hints": hints[:4],
        }

    def _append_run_summary_to_preview(summary):
        preview.append(
            "📊 Run summary: "
            f"evaluated={summary.get('evaluated', 0)} | "
            f"valid_products={summary.get('products_valid', 0)} | "
            f"ideal_unique={summary.get('ideal_unique', 0)} | "
            f"warnings={summary.get('warning', 0)} | "
            f"errors={summary.get('error', 0)}"
        )
        reasons = summary.get("failure_reasons", {}) or {}
        if reasons:
            preview.append("🧭 Top discard/failure reasons:")
            for reason, count in sorted(reasons.items(), key=lambda item: item[1], reverse=True)[:5]:
                preview.append(f"   - {reason}: {count}")
        for hint in summary.get("hints", []) or []:
            preview.append(f"💡 {hint}")

    def _discard_row(core_reagent, failure_reason, comp_name_map=None, comp_smiles_map=None):
        row = {
            "Compatibility_%": "",
            "Molecular_Weight": "",
            "LogP": "",
            "TPSA": "",
            "HBA": "",
            "HBD": "",
            "QED": "",
            "Fsp3": "",
            "PAINS_Alerts": "",
            "Brenk_Alerts": "",
            "Rotatable_Bonds": "",
            "Heavy_Atoms": "",
            "Ring_Count": "",
            "Molar_Refractivity": "",
            "Pass_Lipinski": False,
            "Pass_Ghose": False,
            "Pass_Veber": False,
            "Pass_Egan": False,
            "Pass_Muegge": False,
            "Ideal_Rule": ideal_rule,
            "SMILES_Final": "",
            "InChIKey": "",
            "Is_Duplicate": False,
            "Duplicate_Of": "",
            "Classification": "Discarded",
            "Review_Status": "Error",
            "Core_Reagent": core_reagent,
            "Failure_Reason": failure_reason,
        }
        comp_name_map = comp_name_map or {}
        comp_smiles_map = comp_smiles_map or {}
        row.update({c: comp_name_map.get(c, "") for c in comps})
        row.update({f"{c}_SMILES": comp_smiles_map.get(c, "") for c in comps})
        return row

    results = []
    failed = 0
    total_combinations = 0

    if core_mols and len(listas) >= 1:
        insert_idx = _find_core_insert_index(rxn_variants, listas, core_mols[0][2])
        preview.append(f"ℹ Core reagent insertion index: {insert_idx}")
        preview.append("🧪 Core reagents selected: " + ", ".join([c[0] for c in core_mols]))
        preflight_rows = _preflight_template_summary(insert_idx=insert_idx)
        _append_preflight_to_preview(preflight_rows)

        combos_per_core = 1
        for lst in listas:
            combos_per_core *= max(1, len(lst))
        total_combinations = combos_per_core * len(core_mols)

        done = 0
        for core_name, core_smi, core_mol in core_mols:
            for combo in itertools.product(*listas):
                done += 1
                if progress_cb:
                    progress_cb(done, total_combinations)
                try:
                    moles = []
                    names = []
                    comp_name_map = {}
                    comp_smiles_map = {}
                    for name, smi in combo:
                        m = parse_smiles_flexible(smi, Chem)
                        if len(comp_smiles_map) < len(comps):
                            comp_smiles_map[comps[len(comp_smiles_map)]] = smi
                        if not m or not _safe_sanitize(m):
                            moles = None
                            break
                        moles.append(m)
                        names.append(name)
                        if len(comp_name_map) < len(comps):
                            comp_name_map[comps[len(comp_name_map)]] = name
                    if not moles:
                        failed += 1
                        results.append(_discard_row(core_name, "Invalid reactant (SMILES parse/sanitize failed)", comp_name_map, comp_smiles_map))
                        continue

                    moles.insert(insert_idx, core_mol)
                    names.insert(insert_idx, "Core")

                    prod, reaction_failure = _first_sanitized_reaction_product(moles)
                    if prod is None:
                        failed += 1
                        results.append(_discard_row(core_name, reaction_failure, comp_name_map, comp_smiles_map))
                        continue

                    metrics = _druglikeness_metrics(prod) or {}
                    mw = float(metrics.get("Molecular_Weight") or 0.0)
                    logp = float(metrics.get("LogP") or 0.0)
                    tpsa = float(metrics.get("TPSA") or 0.0)
                    score = max(0, min(100, round(100 - abs(logp - 2.5) * 8 - abs(mw - 350) * 0.05 - abs(tpsa - 90) * 0.1, 1)))

                    if score < threshold:
                        failed += 1
                        row = {
                            "Compatibility_%": score,
                            **metrics,
                            "Ideal_Rule": ideal_rule,
                            "SMILES_Final": Chem.MolToSmiles(prod),
                            "InChIKey": "",
                            "Is_Duplicate": False,
                            "Duplicate_Of": "",
                            "Classification": "Discarded",
                            "Review_Status": "Warning",
                            "Core_Reagent": core_name,
                            "Failure_Reason": f"Below threshold ({threshold:.1f})",
                        }
                        row.update({c: comp_name_map.get(c, "") for c in comps})
                        row.update({f"{c}_SMILES": comp_smiles_map.get(c, "") for c in comps})
                        results.append(row)
                        continue

                    ideal = _passes_selected_rule(metrics)
                    row = {
                        "Compatibility_%": score,
                        **metrics,
                        "Ideal_Rule": ideal_rule,
                        "SMILES_Final": Chem.MolToSmiles(prod),
                        "InChIKey": "",
                        "Is_Duplicate": False,
                        "Duplicate_Of": "",
                        "Classification": "Ideal" if ideal else "Discarded",
                        "Review_Status": "Ideal" if ideal else "Warning",
                        "Core_Reagent": core_name,
                        "Failure_Reason": "" if ideal else _rule_fail_reason(),
                    }
                    row.update({c: comp_name_map.get(c, "") for c in comps})
                    row.update({f"{c}_SMILES": comp_smiles_map.get(c, "") for c in comps})
                    results.append(row)
                except Exception as e:
                    failed += 1
                    row = {
                        "Compatibility_%": "",
                        "Molecular_Weight": "",
                        "LogP": "",
                        "TPSA": "",
                        "HBA": "",
                        "HBD": "",
                        "SMILES_Final": "",
                        "Classification": "Discarded",
                        "Review_Status": "Error",
                        "Core_Reagent": core_name,
                        "Failure_Reason": f"Exception: {str(e)[:140]}",
                    }
                    results.append(row)
    else:
        preflight_rows = _preflight_template_summary(insert_idx=None)
        _append_preflight_to_preview(preflight_rows)
        combos_per_core = 1
        for lst in listas:
            combos_per_core *= max(1, len(lst))
        total_combinations = combos_per_core
        done = 0
        for combo in itertools.product(*listas):
            done += 1
            if progress_cb:
                progress_cb(done, total_combinations)
            try:
                moles = [parse_smiles_flexible(p[1], Chem) for p in combo]
                names = [p[0] for p in combo]
                comp_name_map = {comps[i]: names[i] for i in range(min(len(comps), len(names)))}
                comp_smiles_map = {comps[i]: combo[i][1] for i in range(min(len(comps), len(combo)))}
                if not all(moles):
                    failed += 1
                    results.append(_discard_row("N/A", "Invalid reactant (SMILES parse failed)", comp_name_map, comp_smiles_map))
                    continue
                ok = True
                for m in moles:
                    if not _safe_sanitize(m):
                        ok = False
                        break
                if not ok:
                    failed += 1
                    results.append(_discard_row("N/A", "Invalid reactant (sanitize failed)", comp_name_map, comp_smiles_map))
                    continue
                prod, reaction_failure = _first_sanitized_reaction_product(moles)
                if prod is None:
                    failed += 1
                    results.append(_discard_row("N/A", reaction_failure, comp_name_map, comp_smiles_map))
                    continue

                metrics = _druglikeness_metrics(prod) or {}
                mw = float(metrics.get("Molecular_Weight") or 0.0)
                logp = float(metrics.get("LogP") or 0.0)
                tpsa = float(metrics.get("TPSA") or 0.0)
                score = max(0, min(100, round(100 - abs(logp - 2.5) * 8 - abs(mw - 350) * 0.05 - abs(tpsa - 90) * 0.1, 1)))
                if score < threshold:
                    failed += 1
                    row = {
                        "Compatibility_%": score,
                        **metrics,
                        "Ideal_Rule": ideal_rule,
                        "SMILES_Final": Chem.MolToSmiles(prod),
                        "InChIKey": "",
                        "Is_Duplicate": False,
                        "Duplicate_Of": "",
                        "Classification": "Discarded",
                        "Review_Status": "Warning",
                        "Core_Reagent": "N/A",
                        "Failure_Reason": f"Below threshold ({threshold:.1f})",
                    }
                    row.update({c: comp_name_map.get(c, "") for c in comps})
                    row.update({f"{c}_SMILES": comp_smiles_map.get(c, "") for c in comps})
                    results.append(row)
                    continue

                ideal = _passes_selected_rule(metrics)
                row = {
                    "Compatibility_%": score,
                    **metrics,
                    "Ideal_Rule": ideal_rule,
                    "SMILES_Final": Chem.MolToSmiles(prod),
                    "InChIKey": "",
                    "Is_Duplicate": False,
                    "Duplicate_Of": "",
                    "Classification": "Ideal" if ideal else "Discarded",
                    "Review_Status": "Ideal" if ideal else "Warning",
                    "Core_Reagent": "N/A",
                    "Failure_Reason": "" if ideal else _rule_fail_reason(),
                }
                row.update({c: comp_name_map.get(c, "") for c in comps})
                row.update({f"{c}_SMILES": comp_smiles_map.get(c, "") for c in comps})
                results.append(row)
            except Exception as e:
                failed += 1
                row = {
                    "Compatibility_%": "",
                    "Molecular_Weight": "",
                    "LogP": "",
                    "TPSA": "",
                    "HBA": "",
                    "HBD": "",
                    "SMILES_Final": "",
                    "Classification": "Discarded",
                    "Review_Status": "Error",
                    "Core_Reagent": "N/A",
                    "Failure_Reason": f"Exception: {str(e)[:140]}",
                }
                results.append(row)

    df_all = pd.DataFrame(results) if results else empty_df
    try:
        if "Review_Status" not in df_all.columns:
            if "SMILES_Final" in df_all.columns:
                df_all["Review_Status"] = [
                    "Ideal" if str(row.get("Classification", "")) == "Ideal" else ("Warning" if str(row.get("SMILES_Final", "") or "").strip() else "Error")
                    for _, row in df_all.iterrows()
                ]
            else:
                df_all["Review_Status"] = ""
    except Exception:
        pass

    # Add chirality/stereo summary + InChIKey + duplicate flags (does not change row count).
    try:
        if _CHEM_READY and "SMILES_Final" in df_all.columns:
            # Chirality/stereochemistry (computed from SMILES_Final so it applies to
            # both Ideal and Discarded rows that still have a product).
            try:
                ch_total = []
                ch_def = []
                ch_un = []
                ch_tags = []
                ch_has = []
                for _, r in df_all.iterrows():
                    smi = str(r.get("SMILES_Final", "") or "").strip()
                    if not smi:
                        ch_total.append("")
                        ch_def.append("")
                        ch_un.append("")
                        ch_tags.append("")
                        ch_has.append(False)
                        continue
                    m = parse_smiles_flexible(smi, Chem)
                    if not m:
                        ch_total.append("")
                        ch_def.append("")
                        ch_un.append("")
                        ch_tags.append("")
                        ch_has.append(False)
                        continue
                    cm = _chirality_metrics(m)
                    ch_total.append(cm.get("Chiral_Centers", ""))
                    ch_def.append(cm.get("Chiral_Centers_Defined", ""))
                    ch_un.append(cm.get("Chiral_Centers_Unassigned", ""))
                    ch_tags.append(cm.get("Chiral_Tags", ""))
                    ch_has.append(bool(cm.get("Has_Stereo", False)))

                df_all["Chiral_Centers"] = ch_total
                df_all["Chiral_Centers_Defined"] = ch_def
                df_all["Chiral_Centers_Unassigned"] = ch_un
                df_all["Chiral_Tags"] = ch_tags
                df_all["Has_Stereo"] = ch_has
            except Exception:
                pass

            try:
                from rdkit.Chem.inchi import MolToInchiKey as _MolToInchiKey
            except Exception:
                _MolToInchiKey = None

            first_for_key = {}
            inchis = []
            is_dup = []
            dup_of = []
            for i, r in df_all.iterrows():
                smi = str(r.get("SMILES_Final", "") or "").strip()
                if not smi:
                    inchis.append("")
                    is_dup.append(False)
                    dup_of.append("")
                    continue
                try:
                    mol = parse_smiles_flexible(smi, Chem)
                    if mol is None or _MolToInchiKey is None:
                        ik = ""
                    else:
                        ik = _MolToInchiKey(mol)
                except Exception:
                    ik = ""

                inchis.append(ik)
                if ik and ik in first_for_key:
                    is_dup.append(True)
                    dup_of.append(first_for_key[ik])
                else:
                    is_dup.append(False)
                    dup_of.append("")
                    if ik:
                        first_for_key[ik] = int(i)

            df_all["InChIKey"] = inchis
            df_all["Is_Duplicate"] = is_dup
            df_all["Duplicate_Of"] = dup_of
    except Exception:
        pass

    if len(df_all) != total_combinations and total_combinations > 0:
        preview.append(f"⚠️ Warning: rows({len(df_all)}) != evaluated({total_combinations})")

    df_ideal = df_all[df_all["Classification"] == "Ideal"].copy()
    try:
        if "Is_Duplicate" in df_ideal.columns:
            df_ideal = df_ideal[df_ideal["Is_Duplicate"] != True].copy()
    except Exception:
        pass
    if not df_ideal.empty:
        try:
            df_ideal["Compatibility_%"] = pd.to_numeric(df_ideal["Compatibility_%"], errors="coerce")
        except Exception:
            pass
        df_ideal = df_ideal.sort_values("Compatibility_%", ascending=False)

    summary = _run_summary(df_all, df_ideal)
    _append_run_summary_to_preview(summary)
    preview.append(
        f"✅ {len(df_ideal)} Ideal | ⚠ {summary.get('warning', 0)} Warning | "
        f"❌ {summary.get('error', failed)} Error | 📊 Total evaluated: {total_combinations}"
    )
    try:
        if hasattr(df_all, "attrs"):
            if "_input_qc" in locals():
                df_all.attrs["input_qc"] = _input_qc
            df_all.attrs["preflight"] = preflight_rows if "preflight_rows" in locals() else []
            df_all.attrs["run_summary"] = summary
        if hasattr(df_ideal, "attrs"):
            df_ideal.attrs["run_summary"] = summary
    except Exception:
        pass
    return df_all, df_ideal, "\n".join(preview)
