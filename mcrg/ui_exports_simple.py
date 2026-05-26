from __future__ import annotations


def get_filtered_df(app):
    """Return the dataframe matching the current Results-table filter.

    The Results tab has three views — Ideal / All / Discard — controlled by
    ``app.filter_var``. Lightweight exports (CSV / XLSX / PDF) export only the
    rows belonging to the selected view to avoid blank rows in the output.
    Heavy 3D conformer export keeps its own logic (always Ideal).
    """
    try:
        v = app.filter_var.get() if hasattr(app, "filter_var") else "All"
    except Exception:
        v = "All"

    if v == "Ideal":
        return app.df_ideal
    if v == "Discard":
        df_all = app.df_all
        if df_all is None or getattr(df_all, "empty", True):
            return df_all
        if "Classification" in getattr(df_all, "columns", []):
            return df_all[df_all["Classification"] != "Ideal"]
        return df_all
    return app.df_all


def _filter_suffix(app) -> str:
    """Return a short filename-friendly suffix for the active filter."""
    try:
        v = app.filter_var.get() if hasattr(app, "filter_var") else "All"
    except Exception:
        v = "All"
    v = (v or "All").strip().lower()
    return {"ideal": "ideal", "discard": "discard", "all": "all"}.get(v, "all")


def export_file(app, g: dict, ext: str, save_fn):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]

    df = get_filtered_df(app)
    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return
    initialfile = f"mcrg_results_{_filter_suffix(app)}.{ext}"
    fp = filedialog.asksaveasfilename(
        defaultextension=f".{ext}",
        filetypes=[(ext.upper(), f"*.{ext}")],
        initialfile=initialfile,
    )
    if fp:
        save_fn(df, fp)
        messagebox.showinfo("OK", f"{app.t('saved')} {fp}")


def exp_csv(app, g: dict):
    return export_file(app, g, "csv", lambda df, fp: df.to_csv(fp, index=False))


def exp_xlsx(app, g: dict):
    return export_file(app, g, "xlsx", lambda df, fp: df.to_excel(fp, index=False, engine="openpyxl"))


def exp_pdf(app, g: dict):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]

    df = get_filtered_df(app)
    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return
    initialfile = f"mcrg_results_{_filter_suffix(app)}.pdf"
    fp = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")],
        initialfile=initialfile,
    )
    if not fp:
        return
    app._export_pdf(df, fp)
