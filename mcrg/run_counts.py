from __future__ import annotations


def summarize_results(df_all, df_ideal=None) -> dict:
    if df_all is None or getattr(df_all, "empty", True):
        return {
            "evaluated": 0,
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
        }
    try:
        attrs = getattr(df_all, "attrs", {}) or {}
        summary = attrs.get("run_summary")
        if isinstance(summary, dict):
            return summary.copy()
    except Exception:
        pass
    total = int(len(df_all))
    try:
        ideal_raw = int((df_all["Classification"].astype(str) == "Ideal").sum()) if "Classification" in df_all.columns else 0
    except Exception:
        ideal_raw = 0
    try:
        status = df_all["Review_Status"].fillna("").astype(str) if "Review_Status" in df_all.columns else []
        warning = int((status == "Warning").sum()) if len(status) else 0
        error = int((status == "Error").sum()) if len(status) else 0
    except Exception:
        warning = 0
        error = 0
    try:
        smiles = df_all["SMILES_Final"].fillna("").astype(str) if "SMILES_Final" in df_all.columns else []
        products_valid = int((smiles.str.len() > 0).sum()) if len(smiles) else 0
    except Exception:
        products_valid = 0
    try:
        reasons = df_all["Failure_Reason"].fillna("").astype(str) if "Failure_Reason" in df_all.columns else []
        rule_failed = int(reasons.str.startswith("Fails").sum()) if len(reasons) else 0
        below_threshold = int(reasons.str.startswith("Below threshold").sum()) if len(reasons) else 0
    except Exception:
        rule_failed = 0
        below_threshold = 0
    try:
        duplicates = int((df_all["Is_Duplicate"] == True).sum()) if "Is_Duplicate" in df_all.columns else 0
    except Exception:
        duplicates = 0
    return {
        "evaluated": total,
        "products_valid": products_valid,
        "ideal_raw": ideal_raw,
        "ideal_unique": int(len(df_ideal)) if df_ideal is not None else ideal_raw,
        "warning": warning,
        "error": error,
        "discarded": int(total - ideal_raw),
        "reaction_failed": int(max(0, total - products_valid)),
        "rule_failed": rule_failed,
        "below_threshold": below_threshold,
        "duplicates": duplicates,
    }


def format_run_counter(df_all, df_ideal=None) -> str:
    s = summarize_results(df_all, df_ideal)
    return (
        f"Eval: {s.get('evaluated', 0)} | "
        f"Products: {s.get('products_valid', 0)} | "
        f"Ideal: {s.get('ideal_unique', 0)} | "
        f"Warning: {s.get('warning', 0)} | "
        f"Error: {s.get('error', 0)}"
    )
