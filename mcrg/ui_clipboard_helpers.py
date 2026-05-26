from __future__ import annotations


def get_selected_smiles(app, g: dict):
    sel = app.tree.selection() if hasattr(app, "tree") else ()
    if not sel:
        return []
    cols = list(app.tree["columns"])
    if "SMILES_Final" not in cols:
        return []
    smi_idx = cols.index("SMILES_Final")
    smiles = []
    for iid in sel:
        vals = app.tree.item(iid).get("values") or []
        if smi_idx < len(vals):
            s = str(vals[smi_idx]).strip()
            if s:
                smiles.append(s)
    # Keep order, de-duplicate
    out = []
    seen = set()
    for s in smiles:
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out


def get_ideal_smiles(app, g: dict):
    df = app.df_ideal
    if df is None or getattr(df, "empty", True):
        return []
    if "SMILES_Final" not in df.columns:
        return []
    vals = [str(s).strip() for s in df["SMILES_Final"].tolist() if str(s).strip()]
    out = []
    seen = set()
    for s in vals:
        if s not in seen:
            out.append(s)
            seen.add(s)
    return out


def copy_to_clipboard(app, g: dict, text: str):
    try:
        app.root.clipboard_clear()
        app.root.clipboard_append(text)
        app.root.update_idletasks()
    except Exception:
        pass

