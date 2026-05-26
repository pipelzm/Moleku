from __future__ import annotations

import re
import sys


def _looks_like_smiles(text: str) -> bool:
    s = str(text or "").strip()
    if not s:
        return False
    return any(ch in s for ch in ("C", "c", "N", "n", "O", "o", "S", "s", "P", "p", "=", "#", "(", ")", "[", "]", "@", "/", "\\"))


def _unique_smiles(smiles: list[str], names: list[str] | None = None):
    clean_smiles = []
    clean_names = []
    seen = set()
    for idx, smi in enumerate(smiles):
        s = str(smi or "").strip()
        if not s or s in seen:
            continue
        seen.add(s)
        clean_smiles.append(s)
        if names is not None:
            clean_names.append(str(names[idx] or "").strip())
    return clean_smiles, clean_names if names is not None else None


def _dataframe_from_smiles(smiles: list[str], names: list[str] | None = None):
    try:
        import pandas as pd
    except Exception:
        return None, []

    smiles, names = _unique_smiles(smiles, names)
    if not smiles:
        return None, []
    if names is None:
        names = [f"Candidate_{i+1:03d}" for i in range(len(smiles))]
    else:
        names = [n if n else f"Candidate_{i+1:03d}" for i, n in enumerate(names)]
    df = pd.DataFrame({"Candidate_Name": names, "SMILES_Final": smiles})
    return df, smiles


def _lookup_source_df(app, smiles: list[str], names: list[str] | None = None):
    smiles, names = _unique_smiles(smiles, names)
    if not smiles:
        return None, []

    df_all = getattr(app, "df_all", None)
    if df_all is None or getattr(df_all, "empty", True) or "SMILES_Final" not in getattr(df_all, "columns", []):
        return _dataframe_from_smiles(smiles, names)

    try:
        source_df = df_all[df_all["SMILES_Final"].astype(str).isin(smiles)].copy()
        if getattr(source_df, "empty", True):
            return _dataframe_from_smiles(smiles, names)
        order_map = {s: i for i, s in enumerate(smiles)}
        source_df["__admet_order"] = source_df["SMILES_Final"].astype(str).map(order_map)
        source_df = source_df.sort_values("__admet_order")
        source_df = source_df.drop_duplicates(subset=["SMILES_Final"], keep="first")
        source_df = source_df.drop(columns=["__admet_order"], errors="ignore")
        if names:
            name_map = {s: (names[idx] if idx < len(names) else "") for idx, s in enumerate(smiles)}
            source_df["Candidate_Name"] = source_df["SMILES_Final"].astype(str).map(name_map)
        source_df["Candidate_Name"] = [
            str(v).strip() if str(v).strip() else f"Candidate_{i+1:03d}"
            for i, v in enumerate(source_df.get("Candidate_Name", []))
        ]
        smiles = [str(x) for x in source_df["SMILES_Final"].tolist()]
        return source_df, smiles
    except Exception:
        return _dataframe_from_smiles(smiles, names)


def _smiles_from_tree(app, items):
    try:
        cols = list(app.tree["columns"])
        smi_idx = cols.index("SMILES_Final")
    except Exception:
        return []

    smiles = []
    seen = set()
    for item in items:
        vals = app.tree.item(item).get("values", [])
        if smi_idx >= len(vals):
            continue
        smi = str(vals[smi_idx] or "").strip()
        if smi and smi not in seen:
            seen.add(smi)
            smiles.append(smi)
    return smiles


def _visible_source_df(app):
    try:
        items = app.tree.get_children()
    except Exception:
        return None, []
    smiles = _smiles_from_tree(app, items)
    return _lookup_source_df(app, smiles)


def _selected_source_df(app):
    try:
        selected = app.tree.selection()
    except Exception:
        selected = []
    smiles = _smiles_from_tree(app, selected)
    if smiles:
        return _lookup_source_df(app, smiles)
    return _visible_source_df(app)


def _ideal_source_df(app):
    df_ideal = getattr(app, "df_ideal", None)
    if df_ideal is None or getattr(df_ideal, "empty", True):
        return None, []
    try:
        source_df = df_ideal.copy()
        if "SMILES_Final" not in source_df.columns:
            return None, []
        source_df = source_df.drop_duplicates(subset=["SMILES_Final"], keep="first")
        source_df["Candidate_Name"] = [
            str(v).strip() if str(v).strip() else f"Candidate_{i+1:03d}"
            for i, v in enumerate(source_df.get("Candidate_Name", []))
        ]
        smiles = [str(x).strip() for x in source_df["SMILES_Final"].tolist() if str(x).strip()]
        if not smiles:
            return None, []
        return source_df, smiles
    except Exception:
        return None, []


def _pasted_source_df(smiles_text: str):
    parsed_smiles = []
    parsed_names = []
    for raw in str(smiles_text or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in re.split(r"[\t;,]", line) if p.strip()]
        smi = ""
        name = ""
        if len(parts) >= 2 and _looks_like_smiles(parts[-1]):
            smi = parts[-1]
            name = " ".join(parts[:-1]).strip()
        elif len(parts) >= 2 and _looks_like_smiles(parts[0]):
            smi = parts[0]
            name = " ".join(parts[1:]).strip()
        elif _looks_like_smiles(line):
            smi = line
        if smi:
            parsed_smiles.append(smi)
            parsed_names.append(name)
    return _dataframe_from_smiles(parsed_smiles, parsed_names)


def _normalize_admet_predictions(preds_df, source_smiles: list[str]):
    df = preds_df
    if hasattr(df, "reset_index"):
        df = df.reset_index()

    if df is None or getattr(df, "empty", True):
        return df

    smiles_col = None
    for col in ("SMILES_Final", "SMILES", "smiles", "index"):
        if col not in df.columns:
            continue
        try:
            sample = next((str(v).strip() for v in df[col].tolist() if str(v).strip()), "")
        except Exception:
            sample = ""
        if col != "index" or _looks_like_smiles(sample):
            smiles_col = col
            break

    if smiles_col is not None:
        if smiles_col != "SMILES_Final":
            df.insert(0, "SMILES_Final", df[smiles_col].astype(str))
        for col in ("SMILES", "smiles", "index"):
            if col in df.columns and col != "SMILES_Final":
                try:
                    if df[col].astype(str).equals(df["SMILES_Final"].astype(str)):
                        df = df.drop(columns=[col])
                except Exception:
                    continue
        return df

    if source_smiles and len(source_smiles) == len(df):
        df.insert(0, "SMILES_Final", list(source_smiles))
        return df

    raise ValueError("Could not determine SMILES column in ADMET predictions.")


def _merge_admet_with_source(source_df, preds_df):
    if source_df is None or getattr(source_df, "empty", True):
        return preds_df
    try:
        merged = source_df.merge(preds_df, on="SMILES_Final", how="left", suffixes=("", "_ADMET"))
        return merged
    except Exception:
        return preds_df


def _admet_runtime_message(app, ex: Exception | None = None) -> str:
    if getattr(sys, "frozen", False):
        base = app.t("admet_missing_pkg_app")
    else:
        base = app.t("admet_missing_pkg")
    detail = str(ex or "").strip()
    if not detail:
        return base
    detail_l = detail.lower()
    if any(token in detail_l for token in ("admet", "pkg_resources", "setuptools", "torch", "py4j", "hyperopt", "chemprop")):
        return f"{base}\n\nDetails: {detail}"
    return detail


def _run_admet_prediction(app, g: dict, source_df, smiles: list[str], empty_message: str):
    messagebox = g["messagebox"]
    threading = g["threading"]
    HAS_CTK = g["HAS_CTK"]

    if not smiles:
        messagebox.showinfo("!", empty_message)
        return
    try:
        from admet_ai import ADMETModel
    except Exception as ex:
        messagebox.showerror("Missing Library", _admet_runtime_message(app, ex))
        return

    try:
        txt = app.t("admet_tab_running", n=len(smiles))
        if getattr(app, "lbl_admet_rstats", None):
            (app.lbl_admet_rstats.configure(text=txt) if HAS_CTK else app.lbl_admet_rstats.config(text=txt))
    except Exception:
        pass

    def worker():
        try:
            model = ADMETModel(
                num_workers=0,
                fingerprint_multiprocessing_min=10**9,
            )
            preds = model.predict(smiles=smiles)
            app.root.after(0, lambda: show_admet_predictions(app, g, preds, source_df=source_df, source_smiles=smiles))
        except Exception as ex:
            app.root.after(0, lambda: messagebox.showerror("Error", _admet_runtime_message(app, ex)))

    threading.Thread(target=worker, daemon=True).start()


def admet_copy_selected_smiles(app, g: dict):
    messagebox = g["messagebox"]
    smiles = app._get_selected_smiles()
    if not smiles:
        messagebox.showinfo("!", app.t("admet_no_selection"))
        return
    app._copy_to_clipboard("\n".join(smiles))
    messagebox.showinfo("OK", f"{app.t('admet_clipboard_ok')}\n\nn={len(smiles)}")


def admet_copy_ideal_smiles(app, g: dict):
    messagebox = g["messagebox"]
    smiles = app._get_ideal_smiles()
    if not smiles:
        messagebox.showinfo("!", app.t("no_datos"))
        return
    app._copy_to_clipboard("\n".join(smiles))
    messagebox.showinfo("OK", f"{app.t('admet_clipboard_ok')}\n\nn={len(smiles)}")


def admet_open_web(app, g: dict):
    webbrowser = g["webbrowser"]
    try:
        webbrowser.open("https://admet.ai.greenstonebio.com/")
    except Exception:
        pass


def admet_predict_selected_local(app, g: dict):
    source_df, smiles = _selected_source_df(app)
    return _run_admet_prediction(app, g, source_df, smiles, app.t("admet_tab_no_results_visible"))


def admet_predict_visible_local(app, g: dict):
    source_df, smiles = _visible_source_df(app)
    return _run_admet_prediction(app, g, source_df, smiles, app.t("admet_tab_no_results_visible"))


def admet_predict_ideal_local(app, g: dict):
    source_df, smiles = _ideal_source_df(app)
    return _run_admet_prediction(app, g, source_df, smiles, app.t("admet_tab_no_ideal_results"))


def admet_predict_pasted_local(app, g: dict, smiles_text: str):
    source_df, smiles = _pasted_source_df(smiles_text)
    return _run_admet_prediction(app, g, source_df, smiles, app.t("admet_tab_no_input_smiles"))


def show_admet_predictions(app, g: dict, preds_df, source_df=None, source_smiles=None):
    messagebox = g["messagebox"]
    try:
        df = _normalize_admet_predictions(preds_df, list(source_smiles or []))
        df = _merge_admet_with_source(source_df, df)
    except Exception:
        messagebox.showerror("Error", "Could not format ADMET predictions.")
        return

    try:
        app._last_admet_df = df.copy() if hasattr(df, "copy") else df
        app._last_admet_meta = {"n_rows": int(len(df))}
        try:
            import admet_ai as _admet_ai
            app._last_admet_meta["admet_ai_version"] = getattr(_admet_ai, "__version__", "unknown")
        except Exception:
            app._last_admet_meta["admet_ai_version"] = "unknown"
    except Exception:
        app._last_admet_df = None
        app._last_admet_meta = None
    try:
        app.df_admet_all = df.copy() if hasattr(df, "copy") else df
        app.df_admet_view = app.df_admet_all
        app.admet_search_var.set("")
        app._apply_admet_filter()
        app._switch_tab("admet")
    except Exception as ex:
        messagebox.showerror("Error", str(ex))

