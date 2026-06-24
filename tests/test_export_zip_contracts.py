import json
import zipfile

import pytest


def _has_rdkit_and_pandas():
    try:
        import pandas  # noqa: F401
        from rdkit import Chem  # noqa: F401
        return True
    except Exception:
        return False


class _Var:
    def __init__(self, v):
        self._v = v

    def get(self):
        return self._v

    def set(self, v):
        self._v = v


@pytest.mark.skipif(not _has_rdkit_and_pandas(), reason="rdkit+pandas required for zip export contracts")
def test_paper_dataset_zip_contract(tmp_path):
    import pandas as pd
    import mcrg_desktop as m
    from mcrg_desktop import MCRGApp
    m._load_heavy()

    df = pd.DataFrame(
        [
                {
                    "SMILES_Final": "CCN",
                "Classification": "Ideal",
                "Review_Status": "Ideal",
                "Compatibility_%": 88.0,
                "InChIKey": "",
                "Failure_Reason": "",
            },
            {
                "SMILES_Final": "CCO",
                "Classification": "Discarded",
                "Review_Status": "Warning",
                "Compatibility_%": 10.0,
                "InChIKey": "",
                "Failure_Reason": "Below threshold (50.0)",
            }
        ]
    )

    class Fake:
        df_all = df
        lang_var = _Var("English")
        _last_run_context = {"mcr": "Biginelli (3-CR)", "threshold": 50.0, "ideal_rule": "Lipinski", "standardize": True}

        # minimal i18n helpers used by schema export
        def _col_label(self, c):
            return c

        # avoid generating figures in tests
        def _export_plots_paper_ready(self, folder: str):
            return None

    zip_path = tmp_path / "paper.zip"
    out = MCRGApp._export_paper_dataset_zip(Fake(), str(zip_path))
    assert out["files"] > 0

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())
        # core deliverables
        assert "tables/results_all.csv" in names
        assert "tables/results.sdf" in names
        assert "qc/qc_report.json" in names
        assert "schema/results_schema.json" in names
        assert "env/python_env.json" in names
        assert "env/pip_freeze.txt" in names
        assert "paper_manifest.json" in names
        manifest = json.loads(zf.read("paper_manifest.json").decode("utf-8"))
        assert manifest["ideal_rule"] == "Lipinski"
        assert manifest["standardize"] is True
        sdf_text = zf.read("tables/results.sdf").decode("utf-8", errors="ignore")
        assert "Below threshold (50.0)" in sdf_text


@pytest.mark.skipif(not _has_rdkit_and_pandas(), reason="rdkit+pandas required for zip export contracts")
def test_custom_zip_figures_only_contract(tmp_path):
    from mcrg_desktop import MCRGApp

    class Fake:
        df_all = None
        lang_var = _Var("English")
        _last_run_context = {}

        def _col_label(self, c):
            return c

        def _export_plots_paper_ready(self, folder: str):
            # Create a sentinel file so the zipper picks it up
            import os

            os.makedirs(folder, exist_ok=True)
            with open(os.path.join(folder, "sentinel.txt"), "w", encoding="utf-8") as f:
                f.write("ok\n")

    zip_path = tmp_path / "custom_figures.zip"
    out = MCRGApp._export_paper_dataset_zip(
        Fake(),
        str(zip_path),
        export_options={
            "tables_all": False,
            "tables_ideal": False,
            "tables_descriptors": False,
            "tables_alerts": False,
            "tables_sdf": False,
            "figures": True,
            "qc": False,
            "schema": False,
            "env": False,
        },
        manifest_basename="custom_zip_manifest.json",
    )
    assert out["files"] > 0

    with zipfile.ZipFile(zip_path, "r") as zf:
        names = set(zf.namelist())
        assert "figures/sentinel.txt" in names
        assert "custom_zip_manifest.json" in names
