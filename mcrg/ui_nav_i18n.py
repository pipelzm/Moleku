from __future__ import annotations


def make_hyperlink(app, g: dict, parent, text: str, url: str, font_size: int = 11):
    tk = g["tk"]
    CL = g["CL"]
    FLAT = g["FLAT"]
    LEFT = g["LEFT"]
    webbrowser = g["webbrowser"]

    lbl = tk.Label(
        parent,
        text=text,
        font=app._get_font(font_size, True),
        fg=CL["link"],
        bg=CL["bg"],
        cursor="hand2",
        relief=FLAT,
        bd=0,
        highlightthickness=0,
    )
    lbl.pack(side=LEFT, padx=(0, 4))
    lbl.bind("<Enter>", lambda e: lbl.config(fg="#ff9933"))
    lbl.bind("<Leave>", lambda e: lbl.config(fg=CL["link"]))
    lbl.bind("<Button-1>", lambda e: webbrowser.open(url))
    return lbl


def switch_tab(app, g: dict, tid: str):
    HAS_CTK = g["HAS_CTK"]
    CL = g["CL"]

    app.current_tab = tid
    for _, f in app.tab_frames.items():
        f.grid_remove()
    app.tab_frames[tid].grid(row=0, column=0, sticky="nsew")
    app.root.update_idletasks()
    for t, b in app.tab_btns.items():
        is_active = t == tid
        if HAS_CTK:
            b.configure(
                fg_color=CL["accent"] if is_active else CL["bg3"],
                text_color="#ffffff" if is_active else "#cccccc",
                hover_color=CL["accent2"] if is_active else CL["border"],
            )
        else:
            b.config(
                bg=CL["accent"] if is_active else CL["bg2"],
                fg="#ffffff" if is_active else "#cccccc",
                activebackground=CL["accent2"] if is_active else CL["bg3"],
            )


def on_lang_change(app, g: dict):
    HAS_CTK = g["HAS_CTK"]

    # Update UI language-dependent labels
    app._update_labels()
    app._refresh_slots()
    app._update_preview()
    app._draw_plots()
    app._refresh_results_help_panels()
    if getattr(app, "btn_toggle_results_info", None):
        txt = app.t("results_toggle_info_hide") if getattr(app, "results_info_visible", True) else app.t("results_toggle_info_show")
        (app.btn_toggle_results_info.configure(text=txt) if HAS_CTK else app.btn_toggle_results_info.config(text=txt))


def update_labels(app, g: dict):
    HAS_CTK = g["HAS_CTK"]
    NORMAL = g["NORMAL"]
    DISABLED = g["DISABLED"]
    END = g["END"]

    def _set_attr(name, **kw):
        w = getattr(app, name, None)
        if w and hasattr(w, "configure"):
            w.configure(**kw) if HAS_CTK else w.config(**kw)

    rxn = app.mcr_var.get().split("(")[0].strip()
    tab_map = {
        "motor": app.t("tab_motor", rxn=rxn),
        "resultados": app.t("tab_resultados"),
        "admet": app.t("tab_admet"),
        "espacio": app.t("tab_espacio"),
        "guide": app.t("tab_guide"),
        "acerca": app.t("tab_acerca"),
    }
    for tid, b in app.tab_btns.items():
        b.configure(text=tab_map[tid]) if HAS_CTK else b.config(text=tab_map[tid])

    _set_attr("lbl_title", text=app.t("titulo"))
    _set_attr("lbl_info", text=app.t("info_formato"))
    _set_attr("btn_start", text=app.t("iniciar"))
    _set_attr("btn_clear", text=app.t("limpiar"))
    _set_attr("lbl_thr_t", text=app.t("umbral"))
    _set_attr("lbl_threshold_hint", text=app.t("threshold_hint"))
    _set_attr("lbl_ideal_rule", text=app.t("ideal_rule"))
    _set_attr("lbl_ideal_rule_hint", text=app.t("ideal_rule_hint"))
    _set_attr("btn_table_custom", text=app.t("table_view_custom"))
    _set_attr("lbl_filt", text=app.t("filtro"))
    _set_attr("lbl_2d_title", text=app.t("visor_2d"))
    _set_attr("lbl_esp_t", text=app.t("grafico_titulo"))
    _set_attr("lbl_plot_sel", text=app.t("grafico_sel"))
    _set_attr("btn_export_plot", text=app.t("exportar_alta_calidad"))
    _set_attr("btn_exportar_csv", text=app.t("exportar_csv"))
    _set_attr("btn_exportar_xlsx", text=app.t("exportar_xlsx"))
    _set_attr("btn_exportar_pdf", text=app.t("exportar_pdf"))
    _set_attr("btn_export_table", text=app.t("export_table"))
    _set_attr("btn_exportar_custom_zip", text=app.t("exportar_custom_zip"))
    _set_attr("btn_exportar_zip", text=app.t("exportar_zip"))
    _set_attr("btn_exportar_bundle", text=app.t("exportar_bundle"))
    _set_attr("btn_exportar_paper", text=app.t("exportar_paper"))
    _set_attr("btn_admet_copy_sel", text=app.t("admet_copy_sel"))
    _set_attr("btn_admet_copy_ideal", text=app.t("admet_copy_ideal"))
    _set_attr("btn_admet_open", text=app.t("admet_open_web"))
    _set_attr("btn_admet_predict", text=app.t("admet_predict"))
    try:
        app._refresh_admet_labels()
    except Exception:
        pass

    app._refresh_results_help_panels()
    if getattr(app, "btn_toggle_results_info", None):
        txt = app.t("results_toggle_info_hide") if getattr(app, "results_info_visible", True) else app.t("results_toggle_info_show")
        _set_attr("btn_toggle_results_info", text=txt)

    guide = getattr(app, "guide_text", None)
    if guide:
        guide.config(state=NORMAL)
        guide.delete("1.0", END)
        content = app.t("guide_text")
        for line in content.split("\n"):
            line = line.rstrip()
            if not line:
                guide.insert(END, "\n")
                continue
            if line.startswith("📘") or line.startswith(">") or line.startswith("⚠️") or line.startswith("💡"):
                guide.insert(END, line + "\n", "title")
            elif line.startswith("✅") or line.startswith("📄") or line.startswith("⚗️") or line.startswith("⚙️") or line.startswith("💾"):
                guide.insert(END, line + "\n", "subtitle")
            elif line.startswith("    "):
                guide.insert(END, line + "\n", "code")
            else:
                guide.insert(END, line + "\n")
        guide.config(state=DISABLED)

    combo_plot = getattr(app, "combo_plot", None)
    if combo_plot:
        plot_vals = [app.t(k) for k in app._plot_keys]
        combo_plot.configure(values=plot_vals) if HAS_CTK else combo_plot.config(values=plot_vals)

    if not HAS_CTK:
        for v, rb in getattr(app, "_rbs", []):
            rb.config(text=app.t(v.lower()))

    app.lbl_about_desc.configure(text=app.t("about_desc")) if HAS_CTK else app.lbl_about_desc.config(text=app.t("about_desc"))
    app.lbl_about_footer.configure(text=app.t("about_footer")) if HAS_CTK else app.lbl_about_footer.config(text=app.t("about_footer"))
    app._refresh_table_headings()
    app._switch_tab(app.current_tab)
