import os


def _has_rdkit_and_pandas(m):
    try:
        m._load_heavy()
        return bool(getattr(m, "_CHEM_READY", False)) and getattr(m, "pd", None) is not None
    except Exception:
        return False


def test_catalog_smarts_compile():
    import mcrg_desktop as m

    if not _has_rdkit_and_pandas(m):
        # Skip gracefully if deps are not installed in the environment running tests.
        return

    bad = []
    for k, info in m.MCR_CATALOGO.items():
        smarts_list = [info.get("smarts", "")]
        smarts_list.extend(info.get("smarts_variants", []) or [])
        for idx, smarts in enumerate(smarts_list):
            rxn = m.AllChem.ReactionFromSmarts(smarts)
            if rxn is None:
                bad.append(f"{k}#{idx}")
    assert not bad, f"Invalid reaction SMARTS for: {bad}"


def test_desktop_catalog_uses_modular_core_definitions():
    import mcrg_desktop as m
    from mcrg.catalog import MCR_CATALOGO as modular_catalog

    for key in ("Biginelli (3-CR)", "GBB (3-CR)", "Gewald (3-CR)"):
        assert m.MCR_CATALOGO[key]["smarts"] == modular_catalog[key]["smarts"]
        assert m.MCR_CATALOGO[key].get("smarts_variants", []) == modular_catalog[key].get("smarts_variants", [])


def test_run_mcr_minimal_biginelli_is_deterministic(tmp_path):
    import mcrg_desktop as m

    if not _has_rdkit_and_pandas(m):
        return

    # Minimal single-row input files
    alde = tmp_path / "aldehydes.csv"
    keto = tmp_path / "keto.csv"
    # Use RDKit-parseable SMILES (avoid aromatic/canonical pitfalls).
    alde.write_text("NAME,SMILES\nBenzaldehyde,O=Cc1ccccc1\n", encoding="utf-8")
    keto.write_text("NAME,SMILES\nAcetoacetate,CC(=O)CC(=O)OC\n", encoding="utf-8")

    mcr = "Biginelli (3-CR)"
    files = [str(alde), str(keto)]
    core = [("Urea", "[NH2]C(=O)[NH2]")]

    df1_all, df1_ideal, _ = m.run_mcr(mcr, files, core_smiles_list=core, threshold=0.0, ideal_rule="Lipinski")
    df2_all, df2_ideal, _ = m.run_mcr(mcr, files, core_smiles_list=core, threshold=0.0, ideal_rule="Lipinski")

    assert len(df1_all) == 1
    assert len(df2_all) == 1
    assert df1_all.iloc[0]["SMILES_Final"] == df2_all.iloc[0]["SMILES_Final"]
    assert df1_all.iloc[0]["Core_Reagent"] == "Urea"
    # InChIKey should be computed for products when RDKit InChI is available.
    assert "InChIKey" in df1_all.columns
    assert isinstance(df1_all.iloc[0]["InChIKey"], str)

    # "Ideal" is by Ro5; may be Ideal or Discarded depending on product properties,
    # but it should be consistent and the row must have a product SMILES.
    assert isinstance(df1_all.iloc[0]["SMILES_Final"], str)
    assert len(df1_all.iloc[0]["SMILES_Final"]) > 0
    assert (len(df1_ideal) == len(df2_ideal)) and (len(df1_ideal) in (0, 1))


def test_run_mcr_records_invalid_smiles_as_discarded(tmp_path):
    import mcrg_desktop as m

    if not _has_rdkit_and_pandas(m):
        return

    # Note: cargar_dataframe() filters out invalid SMILES early when RDKit is available.
    # So instead of an invalid SMILES, we use valid reactants that should produce no product
    # under the selected reaction SMARTS, which must be recorded as Discarded.
    alde = tmp_path / "aldehydes.csv"
    keto = tmp_path / "keto.csv"
    alde.write_text("NAME,SMILES\nBenzaldehyde,O=Cc1ccccc1\n", encoding="utf-8")
    # Not a beta-ketoester/enolizable carbonyl suitable for Biginelli in this SMARTS model
    keto.write_text("NAME,SMILES\nEthylAcetate,CC(=O)OCC\n", encoding="utf-8")

    mcr = "Biginelli (3-CR)"
    files = [str(alde), str(keto)]
    core = [("Urea", "[NH2]C(=O)[NH2]")]

    df_all, df_ideal, _ = m.run_mcr(mcr, files, core_smiles_list=core, threshold=0.0, ideal_rule="Lipinski")
    assert len(df_all) == 1
    assert len(df_ideal) == 0
    assert df_all.iloc[0]["Classification"] == "Discarded"
    assert "No products generated" in str(df_all.iloc[0]["Failure_Reason"])
    assert "Is_Duplicate" in df_all.columns
