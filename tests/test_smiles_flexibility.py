from mcrg.smiles_utils import canonicalize_smiles


def _has_rdkit_and_pandas(m):
    try:
        m._load_heavy()
        return bool(getattr(m, "_CHEM_READY", False)) and getattr(m, "pd", None) is not None
    except Exception:
        return False


def test_loader_accepts_multiple_valid_smiles_styles(tmp_path):
    import mcrg_desktop as m

    if not _has_rdkit_and_pandas(m):
        return

    fp = tmp_path / "variants.csv"
    fp.write_text(
        "\n".join(
            [
                "NAME,SMILES",
                "Ibuprofen_1,CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
                "Ibuprofen_2,[C@H](C(O)=O)(C)C1=CC=C(CC(C)C)C=C1",
                "Benzaldehyde,c1ccccc1C=O",
                r"StereoRich,CN1\C(=C(\O)NC2=NC=C(C)S2)C(=O)C2=CC=CC=C2S1(=O)=O",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    df, report, rejected = m.cargar_dataframe_with_report(str(fp), validate_rdkit=True)

    assert len(df) == 4
    assert int(report["rows_valid"]) == 4
    assert int(report["rows_invalid_smiles"]) == 0
    assert getattr(rejected, "empty", False)


def test_headerless_aromatic_smiles_file_is_detected(tmp_path):
    import mcrg_desktop as m

    if not _has_rdkit_and_pandas(m):
        return

    fp = tmp_path / "aromatic_only.smi"
    fp.write_text("c1ccccc1C=O\nCCO\n", encoding="utf-8")

    df, report, rejected = m.cargar_dataframe_with_report(str(fp), validate_rdkit=True)

    assert len(df) == 2
    assert int(report["rows_valid"]) == 2
    assert int(report["rows_invalid_smiles"]) == 0
    assert getattr(rejected, "empty", False)


def test_canonicalization_matches_equivalent_smiles_orders():
    import mcrg_desktop as m

    if not _has_rdkit_and_pandas(m):
        return

    a = canonicalize_smiles("c1ccccc1C=O", m.Chem)
    b = canonicalize_smiles("O=Cc1ccccc1", m.Chem)
    c = canonicalize_smiles("C1=CC=CC=C1C=O", m.Chem)

    assert a
    assert a == b == c
