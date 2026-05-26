import pytest


def _has_pandas():
    try:
        import pandas  # noqa: F401
        return True
    except Exception:
        return False


@pytest.mark.skipif(not _has_pandas(), reason="pandas not available")
def test_cargar_dataframe_accepts_canonical_smiles_and_missing_name(tmp_path):
    from mcrg_desktop import cargar_dataframe

    p = tmp_path / "input.csv"
    p.write_text("Canonical_SMILES\nO=Cc1ccccc1\n", encoding="utf-8")
    df = cargar_dataframe(str(p))
    assert list(df.columns) == ["NAME", "SMILES"]
    assert df.iloc[0]["SMILES"] == "O=Cc1ccccc1"
    assert df.iloc[0]["NAME"].startswith("Mol_")


@pytest.mark.skipif(not _has_pandas(), reason="pandas not available")
def test_cargar_dataframe_accepts_smiles_only_single_column(tmp_path):
    from mcrg_desktop import cargar_dataframe

    p = tmp_path / "input.smi"
    p.write_text("c1ccccc1C=O\nO=Cc1ccccc1\n", encoding="utf-8")
    df = cargar_dataframe(str(p))
    assert list(df.columns) == ["NAME", "SMILES"]
    # best-effort: at least one row should survive as SMILES
    assert df["SMILES"].astype(str).str.len().min() > 0


@pytest.mark.skipif(not _has_pandas(), reason="pandas not available")
def test_cargar_dataframe_with_report_tracks_rejections(tmp_path):
    from mcrg_desktop import cargar_dataframe_with_report

    p = tmp_path / "input.csv"
    p.write_text("NAME,SMILES\nA,\nB,O=Cc1ccccc1\n", encoding="utf-8")
    df, rep, rej = cargar_dataframe_with_report(str(p), validate_rdkit=False)
    assert rep["rows_raw"] == 2
    assert rep["rows_valid"] == 1
    assert len(df) == 1
    assert len(rej) == 1

