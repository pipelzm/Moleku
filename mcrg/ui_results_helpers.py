from __future__ import annotations


def update_results_counter(app, g: dict):
    HAS_CTK = g["HAS_CTK"]

    df = app.df_all
    if df is None or getattr(df, "empty", True):
        txt = "Total: 0 | ✅ Ideal: 0 | ❌ Discarded: 0"
    else:
        try:
            total = int(len(df))
            ideal = int((df["Classification"] == "Ideal").sum()) if "Classification" in df.columns else 0
            disc = total - ideal
        except Exception:
            total, ideal, disc = len(df), 0, 0
        txt = f"Total: {total} | ✅ Ideal: {ideal} | ❌ Discarded: {disc}"
    if hasattr(app, "lbl_results_counter") and app.lbl_results_counter:
        (app.lbl_results_counter.configure(text=txt) if HAS_CTK else app.lbl_results_counter.config(text=txt))


def refresh_results_help_panels(app, g: dict):
    HAS_CTK = g["HAS_CTK"]

    panels = getattr(app, "_results_help_panels", [])
    for p in panels:
        try:
            title_key = p.get("title_key")
            btn = p.get("btn")
            st = p.get("state", {})
            prefix = "▾ " if st.get("visible", True) else "▸ "
            if btn:
                (btn.configure(text=prefix + app.t(title_key)) if HAS_CTK else btn.config(text=prefix + app.t(title_key)))
            set_text = p.get("set_text")
            if callable(set_text):
                set_text()
        except Exception:
            continue


def apply_results_info_layout(app, g: dict):
    RIGHT = g["RIGHT"]
    Y = g["Y"]

    # Hide/show the entire right-side info container and resize the 2D canvas.
    visible = getattr(app, "results_info_visible", True)
    if getattr(app, "fr_param_help", None) is None:
        return
    try:
        if visible:
            if not app.fr_param_help.winfo_ismapped():
                # Keep consistent with the initial layout from ui_results.py
                app.fr_param_help.pack(side=RIGHT, fill=Y, padx=(12, 0))
            target_w = app._canvas_2d_compact_w
        else:
            if app.fr_param_help.winfo_ismapped():
                app.fr_param_help.pack_forget()
            target_w = app._canvas_2d_expanded_w

        try:
            app.canvas_2d.config(width=target_w)
        except Exception:
            pass

        # Force geometry recalculation and redraw current selection
        try:
            app.root.update_idletasks()
        except Exception:
            pass
        try:
            if app.tree.selection():
                app._on_tree_select(None)
        except Exception:
            pass
    except Exception:
        pass


def toggle_results_info_panels(app, g: dict):
    HAS_CTK = g["HAS_CTK"]

    app.results_info_visible = not getattr(app, "results_info_visible", True)
    app._apply_results_info_layout()
    if getattr(app, "btn_toggle_results_info", None):
        txt = app.t("results_toggle_info_hide") if app.results_info_visible else app.t("results_toggle_info_show")
        (app.btn_toggle_results_info.configure(text=txt) if HAS_CTK else app.btn_toggle_results_info.config(text=txt))


def clear_results(app, g: dict):
    HAS_CTK = g["HAS_CTK"]

    app.df_all = app.df_ideal = None
    app.total_generated = app.total_discarded = 0
    for r in app.tree.get_children():
        app.tree.delete(r)
    app.canvas_2d.delete("all")
    app._mol_img_ref = None

    # Clear the stats panel (last selected molecule)
    try:
        for lbl in getattr(app, "stat_labels", {}).values():
            (lbl.configure(text="") if HAS_CTK else lbl.config(text=""))
    except Exception:
        pass

    for cv, _ in app._plot_canvases:
        cv.delete("all")
    app._plot_canvases = []
    (app.lbl_combinations.configure(text="📊 Total: 0 | ✅ Ideal: 0 | ❌ Discarded: 0") if HAS_CTK else app.lbl_combinations.config(text="📊 Total: 0 | ✅ Ideal: 0 | ❌ Discarded: 0"))
    try:
        app._clear_admet_view()
    except Exception:
        pass
    app._update_labels()
    (app.lbl_status.configure(text=app.t("resultados_limpiados")) if HAS_CTK else app.lbl_status.config(text=app.t("resultados_limpiados")))
    app._update_results_counter()

