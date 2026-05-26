from __future__ import annotations

import zipfile
from pathlib import Path

from .smiles_utils import clean_smiles_text, is_valid_smiles_flexible


def cargar_dataframe(filepath: str, pd=None):
    """
    Backwards-compatible loader used by the engine.
    Returns a standardized dataframe with columns NAME, SMILES.
    """
    df, _rep, _rej = cargar_dataframe_with_report(filepath, pd=pd, validate_rdkit=False)
    return df


def cargar_dataframe_with_report(filepath: str, pd=None, *, validate_rdkit: bool = True, Chem=None, _CHEM_READY: bool = False):
    """
    Load an input file and return:
    - df_valid: standardized dataframe with NAME/SMILES
    - report: dict with counts (raw/empty/invalid)
    - rejected_df: rows rejected during loading (with a 'Reject_Reason' column)

    Notes
    - `pd` is injected to avoid import-time hard dependency.
    - RDKit validation is optional and only applied when Chem + _CHEM_READY are provided.
    """
    if pd is None:
        raise ImportError("pandas not loaded.")
    ext = Path(filepath).suffix.lower()

    def _norm_col(c: str) -> str:
        return str(c).strip().replace(" ", "_").replace("-", "_").upper()

    def _looks_like_smiles(s: str) -> bool:
        s = clean_smiles_text(s)
        if not s or len(s) < 2:
            return False
        if s.lower().startswith(("http://", "https://")):
            return False
        return any(
            ch in s
            for ch in ("C", "c", "N", "n", "O", "o", "S", "s", "P", "p", "=", "#", "(", ")", "[", "]", "@", "/", "\\", "+", "-", ".", "1", "2", "3", "4", "5", "6", "7", "8", "9", "%")
        )

    def _standardize_name_smiles(df):
        def _clean_value(v):
            try:
                if pd.isna(v):
                    return ""
            except Exception:
                pass
            return clean_smiles_text(v)

        df = df.copy()
        df.columns = [_norm_col(c) for c in df.columns]

        name_aliases = ["NAME", "NOMBRE", "ID", "IDENTIFIER", "COMPOUND", "COMPOUND_NAME", "MOLECULE", "TITLE", "LABEL"]
        smiles_aliases = [
            "SMILES", "SMILE", "CANONICAL_SMILES", "CANONICALSMILES", "SMILES_CANONICAL", "SMILES_STRING",
            "STRUCTURE", "STRUCTURE_SMILES", "ISOMERIC_SMILES", "CXSMILES", "UNIQUE_SMILES", "MOLECULE_SMILES"
        ]

        name_col = next((c for c in name_aliases if c in df.columns), None)
        smiles_col = next((c for c in smiles_aliases if c in df.columns), None)
        if smiles_col is None and len(df.columns) == 1:
            smiles_col = df.columns[0]

        if smiles_col is None:
            raise ValueError(
                f"Missing SMILES column in {filepath}.\n\n"
                "Accepted headers include: SMILES, Canonical_SMILES, SMILES_String.\n"
                "If your file has a single column of SMILES, it is also supported."
            )

        out = pd.DataFrame()
        out["NAME"] = df[name_col] if name_col is not None else [f"Mol_{i+1}" for i in range(len(df))]
        out["SMILES"] = df[smiles_col]
        out["NAME"] = out["NAME"].apply(_clean_value)
        out["SMILES"] = out["SMILES"].apply(_clean_value)
        return out

    # Read raw
    df_raw = None
    used_sep = None

    if ext == ".numbers":
        try:
            with zipfile.ZipFile(filepath, "r") as zf:
                csv_files = [f for f in zf.namelist() if f.endswith(".csv")]
                if csv_files:
                    with zf.open(csv_files[0]) as cf:
                        df_raw = pd.read_csv(cf, encoding="utf-8-sig")
                else:
                    df_raw = pd.read_excel(filepath, engine="openpyxl")
        except Exception as e:
            raise ValueError(
                "Format .numbers detected.\n\n"
                "For best compatibility, export to .xlsx or .csv from Apple Numbers.\n"
                f"Error: {e}"
            )
    elif ext in (".csv", ".txt", ".tsv", ".dat", ".smi"):
        single_col_aliases = {"SMILES", "SMILE", "CANONICAL_SMILES", "CANONICALSMILES", "SMILES_STRING", "ISOMERIC_SMILES", "CXSMILES"}
        for sep in [",", ";", "\t", " ", "|"]:
            try:
                df_try = pd.read_csv(filepath, sep=sep, encoding="utf-8-sig")
                norm_cols = [_norm_col(c) for c in df_try.columns]
                if any(c in single_col_aliases for c in norm_cols) or len(df_try.columns) == 1:
                    df_raw = df_try
                    used_sep = sep
                    break
            except Exception:
                continue
        if df_raw is None:
            df_raw = pd.read_csv(filepath, encoding="utf-8-sig")

        # Headerless SMILES-only support
        try:
            if df_raw is not None and len(df_raw.columns) == 1:
                col0 = clean_smiles_text(df_raw.columns[0])
                if _norm_col(col0) not in single_col_aliases and _looks_like_smiles(col0):
                    df_raw = pd.read_csv(filepath, sep=used_sep or ",", header=None, names=["SMILES"], encoding="utf-8-sig")
        except Exception:
            pass

    elif ext in (".xlsx", ".xls"):
        try:
            df_raw = pd.read_excel(filepath, engine="openpyxl" if ext == ".xlsx" else None)
        except Exception as e:
            hint = "Install openpyxl for .xlsx." if ext == ".xlsx" else "You may need xlrd for legacy .xls files."
            raise ValueError(f"Failed to read {ext} file: {filepath}\n{hint}\nError: {e}") from e

    elif ext == ".ods":
        try:
            df_raw = pd.read_excel(filepath, engine="odf")
        except Exception as e:
            raise ValueError(f"Failed to read .ods file: {filepath}\nInstall: pip install odfpy\nError: {e}") from e

    elif ext == ".json":
        try:
            df_raw = pd.read_json(filepath)
        except Exception as e:
            raise ValueError(f"Failed to read .json file: {filepath}\nError: {e}") from e
    else:
        raise ValueError(f"Unsupported format: {ext}")

    if df_raw is None:
        raise ValueError(f"Failed to load file: {filepath}")

    n_raw = int(len(df_raw))
    df_std = _standardize_name_smiles(df_raw)

    mask_nonempty = df_std["SMILES"].astype(str).str.len() > 0
    n_empty = int((~mask_nonempty).sum())

    rejected = []
    if n_empty:
        rej = df_std.loc[~mask_nonempty, ["NAME", "SMILES"]].copy()
        rej["Reject_Reason"] = "Empty SMILES"
        rejected.append(rej)
    df_keep = df_std.loc[mask_nonempty].copy()

    n_invalid = 0
    if validate_rdkit and _CHEM_READY and Chem is not None:
        try:
            valid = df_keep["SMILES"].apply(lambda s: is_valid_smiles_flexible(s, Chem))
            n_invalid = int((~valid).sum())
            if n_invalid:
                rej = df_keep.loc[~valid, ["NAME", "SMILES"]].copy()
                rej["Reject_Reason"] = "Invalid SMILES (RDKit)"
                rejected.append(rej)
            df_keep = df_keep.loc[valid].copy()
        except Exception:
            n_invalid = 0

    rejected_df = pd.concat(rejected, ignore_index=True) if rejected else pd.DataFrame(columns=["NAME", "SMILES", "Reject_Reason"])
    report = {
        "path": str(filepath),
        "format": ext,
        "rows_raw": n_raw,
        "rows_nonempty_smiles": int(len(df_std) - n_empty),
        "rows_invalid_smiles": int(n_invalid),
        "rows_valid": int(len(df_keep)),
        "rdkit_validation": bool(validate_rdkit and _CHEM_READY and Chem is not None),
    }
    return df_keep[["NAME", "SMILES"]].copy(), report, rejected_df

