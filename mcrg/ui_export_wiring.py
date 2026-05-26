from __future__ import annotations


def export_paper_dataset_zip(app, g: dict, zip_path: str, export_options: dict | None = None, *, manifest_basename: str | None = None) -> dict:
    _export_paper_dataset_zip_mod = g["_export_paper_dataset_zip_mod"]
    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    Chem = g.get("Chem")
    AllChem = g.get("AllChem")
    pd = g.get("pd")

    if _export_paper_dataset_zip_mod is None:
        raise ImportError("mcrg.exports not available")

    def _col_label_lang(c: str, forced_lang: str) -> str:
        old = app.lang_var.get()
        try:
            app.lang_var.set(forced_lang)
            return app._col_label(c)
        finally:
            try:
                app.lang_var.set(old)
            except Exception:
                pass

    return _export_paper_dataset_zip_mod(
        zip_path,
        df_all=app.df_all,
        lang=app.lang_var.get() if hasattr(app, "lang_var") else "",
        last_run_context=getattr(app, "_last_run_context", {}) or {},
        col_label_fn=_col_label_lang,
        plot_exporter=app._export_plots_paper_ready,
        plot_settings=dict(PLOT_SETTINGS),
        Chem=Chem,
        AllChem=AllChem,
        pd=pd,
        export_options=export_options,
        manifest_basename=manifest_basename,
    )


def export_research_bundle_zip(app, g: dict, zip_path: str) -> dict:
    _export_research_bundle_zip_mod = g["_export_research_bundle_zip_mod"]
    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    MCR_CATALOGO = g["MCR_CATALOGO"]
    Chem = g.get("Chem")
    pd = g.get("pd")

    if _export_research_bundle_zip_mod is None:
        raise ImportError("mcrg.exports not available")

    df_all = app.df_all
    if df_all is None or getattr(df_all, "empty", True):
        raise RuntimeError("No results to export.")
    df_ideal = None
    try:
        if "Classification" in df_all.columns:
            df_ideal = df_all[df_all["Classification"] == "Ideal"].copy()
    except Exception:
        df_ideal = None

    thr = None
    try:
        thr = float(app.threshold_var.get())
    except Exception:
        thr = None

    return _export_research_bundle_zip_mod(
        zip_path,
        df_all=df_all,
        df_ideal=df_ideal,
        catalog=MCR_CATALOGO,
        plot_settings=dict(PLOT_SETTINGS),
        plot_exporter=app._export_plots_paper_ready,
        Chem=Chem,
        pd=pd,
        last_run_context=getattr(app, "_last_run_context", {}) or {},
        current_filter=app.filter_var.get() if hasattr(app, "filter_var") else "",
        current_lang=app.lang_var.get() if hasattr(app, "lang_var") else "",
        current_mcr=app.mcr_var.get() if hasattr(app, "mcr_var") else "",
        current_threshold=thr,
        last_admet_df=getattr(app, "_last_admet_df", None),
        last_admet_meta=getattr(app, "_last_admet_meta", None),
    )

