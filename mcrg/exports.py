from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import platform as _platform
import subprocess
import tempfile
import zipfile
from pathlib import Path

from .smiles_utils import parse_smiles_flexible


def export_paper_dataset_zip(
    zip_path: str,
    *,
    df_all,
    lang: str,
    last_run_context: dict | None,
    col_label_fn,
    plot_exporter,
    plot_settings: dict,
    Chem,
    AllChem=None,
    pd,
    export_options: dict | None = None,
    manifest_basename: str | None = None,
) -> dict:
    _OPT_KEYS = (
        "tables_all",
        "tables_ideal",
        "tables_descriptors",
        "tables_alerts",
        "tables_sdf",
        "figures",
        "qc",
        "schema",
        "env",
    )
    _FULL = {k: True for k in _OPT_KEYS}
    if export_options is None:
        opts = _FULL.copy()
        manifest_name = manifest_basename or "paper_manifest.json"
        export_kind = "paper"
    else:
        opts = {k: bool(export_options.get(k, False)) for k in _OPT_KEYS}
        manifest_name = manifest_basename or "custom_zip_manifest.json"
        export_kind = "custom"

    needs_df = any(opts[k] for k in ("tables_all", "tables_ideal", "tables_descriptors", "tables_alerts", "tables_sdf", "qc", "schema", "env"))
    if needs_df and (df_all is None or getattr(df_all, "empty", True)):
        raise RuntimeError("No results to export.")

    if df_all is not None and not getattr(df_all, "empty", True):
        try:
            if "SMILES_Final" in df_all.columns:
                df_all = df_all.sort_values(by=["SMILES_Final"], kind="mergesort")
        except Exception:
            pass

    df_ideal = None
    if df_all is not None and not getattr(df_all, "empty", True):
        try:
            if "Classification" in df_all.columns:
                df_ideal = df_all[df_all["Classification"] == "Ideal"].copy()
        except Exception:
            df_ideal = None

    def _sha256_file(p: str) -> str:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def _safe_to_csv(df, path):
        try:
            df.to_csv(path, index=False)
        except Exception:
            df.astype(str).to_csv(path, index=False)

    def _env_snapshot(td: str) -> dict:
        env = {
            "python_version": os.sys.version,
            "platform": _platform.platform(),
            "executable": os.sys.executable,
            "lang": lang,
        }
        try:
            res = subprocess.run([os.sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, check=False)
            freeze = res.stdout.strip()
            with open(os.path.join(td, "env", "pip_freeze.txt"), "w", encoding="utf-8") as f:
                f.write(freeze + ("\n" if freeze else ""))
            env["pip_freeze_ok"] = True
        except Exception as e:
            env["pip_freeze_ok"] = False
            env["pip_freeze_error"] = str(e)

        try:
            res = subprocess.run(["conda", "env", "export", "--no-builds"], capture_output=True, text=True, check=False)
            if res.returncode == 0 and res.stdout.strip():
                with open(os.path.join(td, "env", "environment.yml"), "w", encoding="utf-8") as f:
                    f.write(res.stdout)
                env["conda_env_export_ok"] = True
            else:
                env["conda_env_export_ok"] = False
        except Exception:
            env["conda_env_export_ok"] = False

        with open(os.path.join(td, "env", "python_env.json"), "w", encoding="utf-8") as f:
            json.dump(env, f, indent=2, sort_keys=True)
        return env

    def _schema_json(df_cols: list[str]) -> dict:
        schema = {"schema_version": "1.0.0", "generated_at_utc": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z", "columns": []}
        for c in df_cols:
            try:
                label_en = col_label_fn(c, "English")
                label_es = col_label_fn(c, "Español")
            except Exception:
                label_en = c
                label_es = c
            dtype = ""
            try:
                dtype = str(df_all[c].dtype)
            except Exception:
                dtype = ""
            schema["columns"].append({"key": c, "label_en": label_en, "label_es": label_es, "dtype": dtype})
        return schema

    def _qc_report(df) -> dict:
        rep = {
            "n_rows": int(len(df)),
            "n_ideal": int((df["Classification"] == "Ideal").sum()) if "Classification" in df.columns else None,
            "n_discarded": int((df["Classification"] != "Ideal").sum()) if "Classification" in df.columns else None,
            "missing_inchikey": int((df["InChIKey"].astype(str).str.len() == 0).sum()) if "InChIKey" in df.columns else None,
            "discard_reasons": {},
            "descriptor_summary": {},
        }
        if "Failure_Reason" in df.columns:
            try:
                vc = df["Failure_Reason"].fillna("").astype(str).value_counts(dropna=False)
                rep["discard_reasons"] = {str(k): int(v) for k, v in vc.items()}
            except Exception:
                rep["discard_reasons"] = {}
        for col in (
            "Molecular_Weight",
            "LogP",
            "TPSA",
            "HBA",
            "HBD",
            "Rotatable_Bonds",
            "Heavy_Atoms",
            "Ring_Count",
            "Molar_Refractivity",
            "QED",
            "Fsp3",
            "Compatibility_%",
        ):
            if col in df.columns:
                try:
                    s = pd.to_numeric(df[col], errors="coerce")
                    rep["descriptor_summary"][col] = {
                        "count": int(s.count()),
                        "mean": float(s.mean()) if s.count() else None,
                        "std": float(s.std()) if s.count() else None,
                        "min": float(s.min()) if s.count() else None,
                        "max": float(s.max()) if s.count() else None,
                    }
                except Exception:
                    continue
        return rep

    with tempfile.TemporaryDirectory() as td:
        if any(opts[k] for k in ("tables_all", "tables_ideal", "tables_descriptors", "tables_alerts", "tables_sdf")):
            os.makedirs(os.path.join(td, "tables"), exist_ok=True)
        if opts["figures"]:
            os.makedirs(os.path.join(td, "figures"), exist_ok=True)
        if opts["qc"]:
            os.makedirs(os.path.join(td, "qc"), exist_ok=True)
        if opts["schema"]:
            os.makedirs(os.path.join(td, "schema"), exist_ok=True)
        if opts["env"]:
            os.makedirs(os.path.join(td, "env"), exist_ok=True)

        csv_all = os.path.join(td, "tables", "results_all.csv")
        csv_ideal = os.path.join(td, "tables", "results_ideal.csv")
        sdf_path = os.path.join(td, "tables", "results.sdf")
        sdf3d_zip_path = os.path.join(td, "tables", "structures_3d.zip")

        if df_all is not None:
            if opts["tables_all"]:
                _safe_to_csv(df_all, csv_all)
            if opts["tables_ideal"] and df_ideal is not None and not getattr(df_ideal, "empty", True):
                _safe_to_csv(df_ideal, csv_ideal)

            desc_cols = [c for c in ("SMILES_Final", "InChIKey", "Classification", "Compatibility_%", "Molecular_Weight", "LogP", "TPSA", "HBA", "HBD", "Rotatable_Bonds", "Heavy_Atoms", "Ring_Count", "Molar_Refractivity", "QED", "Fsp3") if c in df_all.columns]
            alerts_cols = [c for c in ("SMILES_Final", "InChIKey", "Classification", "PAINS_Alerts", "Brenk_Alerts") if c in df_all.columns]
            if opts["tables_descriptors"] and desc_cols:
                _safe_to_csv(df_all[desc_cols].copy(), os.path.join(td, "tables", "descriptors.csv"))
            if opts["tables_alerts"] and alerts_cols:
                _safe_to_csv(df_all[alerts_cols].copy(), os.path.join(td, "tables", "medchem_alerts.csv"))

            if opts["tables_sdf"]:
                df_sdf = df_ideal if (df_ideal is not None and not getattr(df_ideal, "empty", True)) else df_all
                try:
                    w = Chem.SDWriter(sdf_path)
                    if "SMILES_Final" in df_sdf.columns:
                        for _, row in df_sdf.iterrows():
                            smi = str(row.get("SMILES_Final", "") or "").strip()
                            mol = parse_smiles_flexible(smi, Chem) if smi else None
                            if mol is None:
                                continue
                            for col in df_sdf.columns:
                                try:
                                    v = row.get(col, "")
                                    if v is None:
                                        v = ""
                                    mol.SetProp(str(col), str(v))
                                except Exception:
                                    continue
                            w.write(mol)
                    w.close()
                except Exception:
                    try:
                        with open(sdf_path, "w", encoding="utf-8") as f:
                            f.write("")
                    except Exception:
                        pass

                # Also include 3D conformers as a zipped SDF (best-effort).
                if AllChem is not None:
                    try:
                        import zipfile as _zipfile

                        sdf3d = os.path.join(td, "tables", "results_3d.sdf")
                        w3 = Chem.SDWriter(sdf3d)
                        if "SMILES_Final" in df_sdf.columns:
                            for _, row in df_sdf.iterrows():
                                smi = str(row.get("SMILES_Final", "") or "").strip()
                                mol = parse_smiles_flexible(smi, Chem) if smi else None
                                if mol is None:
                                    continue
                                mol = Chem.AddHs(mol)
                                ok = 1
                                try:
                                    params = AllChem.ETKDGv3()
                                    params.randomSeed = 42
                                    ok = AllChem.EmbedMolecule(mol, params)
                                except Exception:
                                    ok = 1
                                if ok != 0:
                                    try:
                                        params2 = AllChem.ETKDGv3()
                                        params2.randomSeed = 42
                                        params2.useRandomCoords = True
                                        ok = AllChem.EmbedMolecule(mol, params2)
                                    except Exception:
                                        ok = ok
                                if ok == 0:
                                    try:
                                        try:
                                            AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
                                        except Exception:
                                            AllChem.UFFOptimizeMolecule(mol, maxIters=200)
                                    except Exception:
                                        pass
                                for col in df_sdf.columns:
                                    try:
                                        v = row.get(col, "")
                                        if v is None:
                                            v = ""
                                        mol.SetProp(str(col), str(v))
                                    except Exception:
                                        continue
                                w3.write(mol)
                        w3.close()
                        with _zipfile.ZipFile(sdf3d_zip_path, "w", compression=_zipfile.ZIP_DEFLATED) as z:
                            z.write(sdf3d, arcname="results_3d.sdf")
                    except Exception:
                        try:
                            with open(sdf3d_zip_path, "wb") as f:
                                f.write(b"")
                        except Exception:
                            pass

        if opts["figures"]:
            try:
                plot_exporter(os.path.join(td, "figures"))
            except Exception:
                pass

        if opts["qc"] and df_all is not None:
            qc = _qc_report(df_all)
            with open(os.path.join(td, "qc", "qc_report.json"), "w", encoding="utf-8") as f:
                json.dump(qc, f, indent=2, sort_keys=True)
            try:
                if qc.get("discard_reasons"):
                    r = pd.DataFrame([{"Failure_Reason": k, "Count": v} for k, v in qc["discard_reasons"].items()])
                    r.to_csv(os.path.join(td, "qc", "discard_reasons.csv"), index=False)
            except Exception:
                pass

        if opts["schema"] and df_all is not None:
            schema = _schema_json(list(df_all.columns))
            with open(os.path.join(td, "schema", "results_schema.json"), "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=2, sort_keys=True)

        env = _env_snapshot(td) if opts["env"] else {}

        ctx = last_run_context or {}
        manifest = {
            "paper_dataset_version": "1.0.0",
            "export_kind": export_kind,
            "generated_at_utc": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "lang": lang,
            "mcr": ctx.get("mcr", ""),
            "threshold": ctx.get("threshold", None),
            "ideal_rule": ctx.get("ideal_rule", None),
            "n_rows": int(len(df_all)) if df_all is not None else 0,
            "selection": opts,
            "files": {},
            "env": env if opts["env"] else {},
        }

        manifest_path = os.path.join(td, manifest_name)
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, sort_keys=True)

        fixed_dt = (2020, 1, 1, 0, 0, 0)
        files_added = 0

        def _zip_add(zf, file_path, arcname):
            nonlocal files_added
            if not os.path.exists(file_path):
                return
            zi = zipfile.ZipInfo(arcname, date_time=fixed_dt)
            zi.compress_type = zipfile.ZIP_DEFLATED
            with open(file_path, "rb") as f:
                zf.writestr(zi, f.read())
            files_added += 1
            try:
                manifest["files"][arcname] = {"sha256": _sha256_file(file_path)}
            except Exception:
                manifest["files"][arcname] = {"sha256": ""}

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            if opts["tables_all"]:
                _zip_add(zf, csv_all, "tables/results_all.csv")
            if opts["tables_ideal"]:
                _zip_add(zf, csv_ideal, "tables/results_ideal.csv")
            if opts["tables_descriptors"]:
                _zip_add(zf, os.path.join(td, "tables", "descriptors.csv"), "tables/descriptors.csv")
            if opts["tables_alerts"]:
                _zip_add(zf, os.path.join(td, "tables", "medchem_alerts.csv"), "tables/medchem_alerts.csv")
            if opts["tables_sdf"]:
                _zip_add(zf, sdf_path, "tables/results.sdf")

            if opts["qc"]:
                _zip_add(zf, os.path.join(td, "qc", "qc_report.json"), "qc/qc_report.json")
                _zip_add(zf, os.path.join(td, "qc", "discard_reasons.csv"), "qc/discard_reasons.csv")
            if opts["schema"]:
                _zip_add(zf, os.path.join(td, "schema", "results_schema.json"), "schema/results_schema.json")
            if opts["env"]:
                _zip_add(zf, os.path.join(td, "env", "python_env.json"), "env/python_env.json")
                _zip_add(zf, os.path.join(td, "env", "pip_freeze.txt"), "env/pip_freeze.txt")
                _zip_add(zf, os.path.join(td, "env", "environment.yml"), "env/environment.yml")

            if opts["figures"]:
                try:
                    for root, _dirs, files in os.walk(os.path.join(td, "figures")):
                        for fn in sorted(files):
                            p = os.path.join(root, fn)
                            rel = os.path.relpath(p, td).replace("\\", "/")
                            _zip_add(zf, p, rel)
                except Exception:
                    pass

            try:
                with open(manifest_path, "w", encoding="utf-8") as f:
                    json.dump(manifest, f, indent=2, sort_keys=True)
            except Exception:
                pass
            _zip_add(zf, manifest_path, manifest_name)

        return {"files": files_added}


def export_research_bundle_zip(
    zip_path: str,
    *,
    df_all,
    df_ideal,
    catalog: dict,
    plot_settings: dict,
    plot_exporter,
    Chem,
    pd,
    last_run_context: dict | None,
    current_filter: str,
    current_lang: str,
    current_mcr: str,
    current_threshold: float | None,
    last_admet_df=None,
    last_admet_meta: dict | None = None,
) -> dict:
    if df_all is None or getattr(df_all, "empty", True):
        raise RuntimeError("No results to export.")

    # Deterministic order
    try:
        if "SMILES_Final" in df_all.columns:
            df_all = df_all.sort_values(by=["SMILES_Final"], kind="mergesort")
    except Exception:
        pass

    def _sha256_file(p: str) -> str:
        h = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                h.update(chunk)
        return h.hexdigest()

    def _catalog_sha256() -> str:
        try:
            payload = json.dumps(catalog, sort_keys=True, ensure_ascii=False).encode("utf-8")
            return hashlib.sha256(payload).hexdigest()
        except Exception:
            return ""

    ctx = last_run_context or {}
    component_files = ctx.get("component_files", {}) or {}
    file_hashes = {}
    for comp, p in component_files.items():
        try:
            if p and os.path.isfile(p):
                file_hashes[comp] = {"path": os.path.abspath(p), "sha256": _sha256_file(p), "size": os.path.getsize(p)}
        except Exception:
            continue

    with tempfile.TemporaryDirectory(prefix="mcrg_bundle_") as td:
        inputs_dir = os.path.join(td, "inputs")
        os.makedirs(inputs_dir, exist_ok=True)
        input_copies = {}
        for comp, meta in file_hashes.items():
            try:
                src = meta.get("path")
                if not src or not os.path.isfile(src):
                    continue
                ext = Path(src).suffix or ".txt"
                safe_comp = str(comp).replace("/", "_")
                dst_name = f"{safe_comp}{ext}"
                dst = os.path.join(inputs_dir, dst_name)
                with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                    fdst.write(fsrc.read())
                input_copies[comp] = {"bundle_path": f"inputs/{dst_name}", "sha256": meta.get("sha256", ""), "size": meta.get("size", None)}
            except Exception:
                continue

        csv_all = os.path.join(td, "results_all.csv")
        df_all.to_csv(csv_all, index=False)
        csv_ideal = None
        if df_ideal is not None and not getattr(df_ideal, "empty", True):
            csv_ideal = os.path.join(td, "results_ideal.csv")
            df_ideal.to_csv(csv_ideal, index=False)

        sdf_path = os.path.join(td, "results.sdf")
        df_sdf = df_ideal if (df_ideal is not None and not getattr(df_ideal, "empty", True)) else df_all
        written = 0
        skipped = 0
        if "SMILES_Final" in df_sdf.columns:
            w = Chem.SDWriter(sdf_path)
            try:
                for _, row in df_sdf.iterrows():
                    smi = row.get("SMILES_Final", "")
                    if not smi:
                        skipped += 1
                        continue
                    mol = parse_smiles_flexible(str(smi), Chem)
                    if not mol:
                        skipped += 1
                        continue
                    for col in df_sdf.columns:
                        try:
                            v = row.get(col, "")
                            if v is None:
                                v = ""
                            mol.SetProp(str(col), str(v))
                        except Exception:
                            continue
                    w.write(mol)
                    written += 1
            finally:
                try:
                    w.close()
                except Exception:
                    pass
        else:
            with open(sdf_path, "w", encoding="utf-8") as f:
                f.write("")

        plots_dir = os.path.join(td, "plots")
        os.makedirs(plots_dir, exist_ok=True)
        plots_ok = False
        try:
            plot_exporter(plots_dir)
            plots_ok = True
        except Exception:
            plots_ok = False

        admet_csv = None
        admet_ok = False
        try:
            adf = last_admet_df
            if adf is not None and not getattr(adf, "empty", False):
                admet_dir = os.path.join(td, "admet")
                os.makedirs(admet_dir, exist_ok=True)
                admet_csv = os.path.join(admet_dir, "admet_predictions.csv")
                adf.to_csv(admet_csv, index=False)
                admet_ok = True
        except Exception:
            admet_ok = False

        manifest = {
            "tool": "Moleku",
            "bundle_version": 1,
            "created_utc": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
            "catalog": {"sha256": _catalog_sha256()},
            "run_context": {
                "mcr": ctx.get("mcr", current_mcr),
                "threshold": ctx.get("threshold", current_threshold),
                "core_reagents": ctx.get("core_reagents", []),
                "filter_view": current_filter,
                "lang": current_lang,
            },
            "inputs": {"component_files": file_hashes, "bundle_copies": input_copies},
            "stats": {
                "rows_all": int(len(df_all)),
                "rows_ideal": int(len(df_ideal)) if df_ideal is not None else 0,
                "sdf_written": int(written),
                "sdf_skipped": int(skipped),
                "plots_exported": bool(plots_ok),
                "admet_exported": bool(admet_ok),
            },
            "environment": {"python": os.sys.version.split()[0], "platform": _platform.platform()},
            "plot_settings": dict(plot_settings),
        }
        if admet_ok:
            try:
                manifest["admet"] = (last_admet_meta or {}).copy()
                manifest["admet"]["csv_path"] = "admet/admet_predictions.csv"
            except Exception:
                pass
        try:
            manifest["environment"]["rdkit"] = getattr(Chem, "__version__", "unknown") if Chem else "unavailable"
        except Exception:
            pass

        manifest_path = os.path.join(td, "run_manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

        def _zip_add(zf, file_path, arcname):
            info = zipfile.ZipInfo(arcname)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            with open(file_path, "rb") as f:
                zf.writestr(info, f.read())

        files_added = 0
        with zipfile.ZipFile(zip_path, "w") as zf:
            if os.path.isdir(inputs_dir):
                for fn in sorted(os.listdir(inputs_dir)):
                    p = os.path.join(inputs_dir, fn)
                    if os.path.isfile(p):
                        _zip_add(zf, p, f"inputs/{fn}")
                        files_added += 1
            _zip_add(zf, csv_all, "results/results_all.csv"); files_added += 1
            if csv_ideal and os.path.exists(csv_ideal):
                _zip_add(zf, csv_ideal, "results/results_ideal.csv"); files_added += 1
            _zip_add(zf, sdf_path, "results/results.sdf"); files_added += 1
            _zip_add(zf, manifest_path, "run_manifest.json"); files_added += 1

            if os.path.isdir(plots_dir):
                for root, _dirs, files in os.walk(plots_dir):
                    for fn in sorted(files):
                        p = os.path.join(root, fn)
                        rel = os.path.relpath(p, td).replace("\\", "/")
                        _zip_add(zf, p, rel)
                        files_added += 1

            if admet_ok and admet_csv and os.path.exists(admet_csv):
                _zip_add(zf, admet_csv, "admet/admet_predictions.csv")
                files_added += 1

        return {"files": files_added}

