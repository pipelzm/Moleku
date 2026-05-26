from __future__ import annotations


def show_table_columns_dialog(app, g: dict):
    tk = g["tk"]
    CL = g["CL"]
    BooleanVar = g["BooleanVar"]
    VERTICAL = g["VERTICAL"]
    LEFT = g["LEFT"]
    RIGHT = g["RIGHT"]
    BOTH = g["BOTH"]
    X = g["X"]
    Y = g["Y"]

    top = tk.Toplevel(app.root)
    top.title(app.t("table_cols_title"))
    top.configure(bg=CL["bg"])
    top.geometry("520x520")
    top.resizable(False, False)

    df = app.df_all
    df_cols = list(df.columns) if df is not None and not getattr(df, "empty", True) else []

    preferred = [
        "Compatibility_%",
        "Classification",
        "Failure_Reason",
        "SMILES_Final",
        # Chirality / stereochemistry
        "Has_Stereo",
        "Chiral_Centers",
        "Chiral_Centers_Defined",
        "Chiral_Centers_Unassigned",
        "Chiral_Tags",
        "InChIKey",
        "Is_Duplicate",
        "Duplicate_Of",
        "Core_Reagent",
        "Ideal_Rule",
        "Molecular_Weight",
        "LogP",
        "TPSA",
        "HBA",
        "HBD",
        "Rotatable_Bonds",
        "Heavy_Atoms",
        "Ring_Count",
        "Molar_Refractivity",
        "QED",
        "Fsp3",
        "PAINS_Alerts",
        "Brenk_Alerts",
        "Pass_Lipinski",
        "Pass_Ghose",
        "Pass_Veber",
        "Pass_Egan",
        "Pass_Muegge",
    ]
    candidates = [c for c in preferred if (not df_cols) or (c in df_cols)]
    if df_cols:
        for c in df_cols:
            if c not in candidates:
                candidates.append(c)

    canvas = tk.Canvas(top, bg=CL["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(top, orient=VERTICAL, command=canvas.yview)
    body = tk.Frame(canvas, bg=CL["bg"])
    body.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=body, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    selected = set(app._custom_table_cols or candidates[:8])
    vars_map = {}
    for c in candidates:
        v = BooleanVar(value=(c in selected))
        vars_map[c] = v
        tk.Checkbutton(
            body,
            text=app._col_label(c),
            variable=v,
            bg=CL["bg"],
            fg=CL["fg"],
            selectcolor=CL["bg2"],
            activebackground=CL["bg"],
            font=app._get_font(12),
            anchor="w",
            justify="left",
            highlightthickness=0,
        ).pack(fill=X, padx=12, pady=2)

    fr_btn = tk.Frame(body, bg=CL["bg"])
    fr_btn.pack(fill=X, padx=12, pady=(10, 10))

    def apply():
        cols = [c for c in candidates if vars_map[c].get()]
        if "SMILES_Final" in candidates and "SMILES_Final" not in cols:
            cols.append("SMILES_Final")
        app._custom_table_cols = cols
        top.destroy()
        app._apply_filter()

    tk.Button(fr_btn, text=app.t("table_cols_apply"), command=apply, bg=CL["accent"], fg="#000000", relief="flat").pack(fill=X, pady=(0, 6))
    tk.Button(fr_btn, text=app.t("table_cols_cancel"), command=top.destroy, bg=CL["bg3"], fg=CL["fg"], relief="flat").pack(fill=X)


def show_custom_zip_dialog(app, g: dict):
    tk = g["tk"]
    CL = g["CL"]
    BooleanVar = g["BooleanVar"]
    _CHEM_READY = g["_CHEM_READY"]
    pd = g["pd"]
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]
    threading = g["threading"]
    BOTH = g["BOTH"]
    LEFT = g["LEFT"]
    W = g["W"]
    X = g["X"]
    FLAT = g["FLAT"]

    if not _CHEM_READY or pd is None:
        messagebox.showerror("Error", "RDKit + pandas required")
        return

    ALL_KEYS = (
        "tables_all",
        "tables_ideal",
        "tables_descriptors",
        "tables_alerts",
        "tables_sdf",
        "figures",
        "qc",
        "schema",
        "env",
    )
    top = tk.Toplevel(app.root)
    top.title(app.t("custom_zip_title"))
    top.configure(bg=CL["bg"])
    top.geometry("560x560")
    top.resizable(False, False)

    tk.Label(
        top,
        text=app.t("custom_zip_hint"),
        bg=CL["bg"],
        fg=CL["fg"],
        font=app._get_font(11),
        wraplength=520,
        justify=LEFT,
    ).pack(anchor=W, padx=14, pady=(12, 8))

    vars_map = {}
    labels = {
        "tables_all": "custom_zip_tables_all",
        "tables_ideal": "custom_zip_tables_ideal",
        "tables_descriptors": "custom_zip_descriptors",
        "tables_alerts": "custom_zip_alerts",
        "tables_sdf": "custom_zip_sdf",
        "figures": "custom_zip_figures",
        "qc": "custom_zip_qc",
        "schema": "custom_zip_schema",
        "env": "custom_zip_env",
    }
    body = tk.Frame(top, bg=CL["bg"])
    body.pack(fill=BOTH, expand=True, padx=14, pady=(0, 8))
    for k in ALL_KEYS:
        v = BooleanVar(value=False)
        vars_map[k] = v
        tk.Checkbutton(
            body,
            text=app.t(labels[k]),
            variable=v,
            bg=CL["bg"],
            fg=CL["fg"],
            selectcolor=CL["bg2"],
            activebackground=CL["bg"],
            font=app._get_font(12),
            anchor="w",
            justify="left",
            highlightthickness=0,
        ).pack(fill=X, pady=3)

    preset_fr = tk.Frame(top, bg=CL["bg"])
    preset_fr.pack(fill=X, padx=14, pady=(4, 8))

    def _set_all(on: bool):
        for vv in vars_map.values():
            vv.set(on)

    def _preset_paper():
        _set_all(True)

    def _preset_tables():
        _set_all(False)
        for kk in ("tables_all", "tables_ideal", "tables_descriptors", "tables_alerts", "tables_sdf"):
            vars_map[kk].set(True)

    def _preset_figures():
        _set_all(False)
        vars_map["figures"].set(True)

    for txt, cmd in [
        ("custom_zip_preset_paper", _preset_paper),
        ("custom_zip_preset_tables", _preset_tables),
        ("custom_zip_preset_figures", _preset_figures),
    ]:
        tk.Button(
            preset_fr,
            text=app.t(txt),
            command=cmd,
            bg=CL["bg3"],
            fg=CL["fg"],
            relief=FLAT,
            padx=10,
            pady=4,
        ).pack(side=LEFT, padx=(0, 8))

    btn_fr = tk.Frame(top, bg=CL["bg"])
    btn_fr.pack(fill=X, padx=14, pady=(8, 14))

    def do_export():
        opts = {k: bool(vars_map[k].get()) for k in ALL_KEYS}
        if not any(opts.values()):
            messagebox.showinfo("!", app.t("custom_zip_need_option"))
            return
        needs_df = any(
            opts[k]
            for k in (
                "tables_all",
                "tables_ideal",
                "tables_descriptors",
                "tables_alerts",
                "tables_sdf",
                "qc",
                "schema",
                "env",
            )
        )
        if needs_df and (app.df_all is None or getattr(app.df_all, "empty", True)):
            messagebox.showinfo("!", app.t("custom_zip_need_results"))
            return
        top.destroy()
        fp = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP", "*.zip")])
        if not fp:
            return

        def worker():
            try:
                out = app._export_paper_dataset_zip(fp, export_options=opts, manifest_basename="custom_zip_manifest.json")
                app.root.after(0, lambda: messagebox.showinfo("OK", f"{app.t('saved')} {fp}\n\nFiles: {out.get('files', 0)}"))
            except Exception as ex:
                app.root.after(0, lambda: messagebox.showerror("Error", str(ex)))

        threading.Thread(target=worker, daemon=True).start()

    tk.Button(btn_fr, text=app.t("custom_zip_export"), command=do_export, bg=CL["accent"], fg="#000000", relief=FLAT).pack(fill=X, pady=(0, 6))
    tk.Button(btn_fr, text=app.t("custom_zip_cancel"), command=top.destroy, bg=CL["bg3"], fg=CL["fg"], relief=FLAT).pack(fill=X)


def show_plot_settings(app, g: dict):
    tk = g["tk"]
    ttk = g["ttk"]
    CL = g["CL"]
    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    VERTICAL = g["VERTICAL"]
    LEFT = g["LEFT"]
    RIGHT = g["RIGHT"]
    BOTH = g["BOTH"]
    X = g["X"]
    Y = g["Y"]
    W = g["W"]
    E = g["E"]
    HORIZONTAL = g["HORIZONTAL"]
    StringVar = g["StringVar"]
    BooleanVar = g["BooleanVar"]
    IntVar = g["IntVar"]
    DoubleVar = g["DoubleVar"]
    colorchooser = g["colorchooser"]

    top = tk.Toplevel(app.root)
    lang = app.lang_var.get()
    I18N = {
        "English": {
            "title": "⚙ Advanced Plot Settings",
            "sec_colors": "Colors & Theme",
            "sec_typo": "Typography & Labels",
            "sec_graphics": "Graphic Elements",
            "sec_axes": "Axes & Factors",
            "sec_export": "Export Quality (DPI)",
            "ideal_points": "Ideal Points:",
            "discard_points": "Discarded Points:",
            "axis_lines": "Axis Lines:",
            "grid_lines": "Grid Lines:",
            "plot_bg": "Plot Background:",
            "font_size": "Font Size (pt):",
            "bold_labels": "Bold Font for Labels",
            "marker_size": "Marker Size:",
            "line_width": "Line Width (data):",
            "axis_width": "Axis Line Width:",
            "grid_width": "Grid Line Width:",
            "dist_style": "Distribution Style:",
            "gauss": "Gaussian curve (histogram)",
            "dots_axis": "Dot plot axis line",
            "show_grid": "Show Grid",
            "show_legend": "Show Legend",
            "legend_pos": "Legend Position:",
            "tick_factors": "Number of Tick Factors:",
            "export_dpi": "Export Resolution (DPI):",
            "quick_presets": "Quick presets:",
            "apply": "✓ Apply & Close",
            "cancel": "✕ Cancel",
            "dist_styles": ["Bars", "Dots", "Box"],
            "legend_positions": ["upper left", "upper right", "lower left", "lower right", "center"],
        },
        "Español": {
            "title": "⚙ Configuración avanzada de gráficos",
            "sec_colors": "Colores y tema",
            "sec_typo": "Tipografía y etiquetas",
            "sec_graphics": "Elementos gráficos",
            "sec_axes": "Ejes y factores",
            "sec_export": "Calidad de exportación (DPI)",
            "ideal_points": "Puntos ideales:",
            "discard_points": "Puntos descartados:",
            "axis_lines": "Líneas de ejes:",
            "grid_lines": "Líneas de grilla:",
            "plot_bg": "Fondo del gráfico:",
            "font_size": "Tamaño de letra (pt):",
            "bold_labels": "Texto en negrita",
            "marker_size": "Tamaño del marcador:",
            "line_width": "Grosor de línea (datos):",
            "axis_width": "Grosor de eje:",
            "grid_width": "Grosor de grilla:",
            "dist_style": "Tipo de distribución:",
            "gauss": "Campana de Gauss (histograma)",
            "dots_axis": "Línea de eje en modo pelotas",
            "show_grid": "Mostrar grilla",
            "show_legend": "Mostrar leyenda",
            "legend_pos": "Posición de leyenda:",
            "tick_factors": "Nº de marcas (ticks):",
            "export_dpi": "Resolución de exportación (DPI):",
            "quick_presets": "Preajustes rápidos:",
            "apply": "✓ Aplicar y cerrar",
            "cancel": "✕ Cancelar",
            "dist_styles": ["Barras", "Pelotas", "Caja"],
            "legend_positions": ["arriba izquierda", "arriba derecha", "abajo izquierda", "abajo derecha", "centro"],
        },
    }
    T = I18N.get(lang, I18N["English"])
    top.title(T["title"])
    top.configure(bg=CL["bg"])
    top.geometry("520x520")
    top.resizable(False, False)

    canvas = tk.Canvas(top, bg=CL["bg"], highlightthickness=0)
    scrollbar = tk.Scrollbar(top, orient=VERTICAL, command=canvas.yview)
    scrollable = tk.Frame(canvas, bg=CL["bg"])
    scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)

    def _themed_button(parent, **kwargs):
        base = {
            "bg": CL["bg3"],
            "fg": CL["fg"],
            "activebackground": CL["border"],
            "activeforeground": CL["fg"],
            "relief": "flat",
            "bd": 0,
            "highlightthickness": 0,
            "cursor": "hand2",
        }
        base.update(kwargs)
        return tk.Button(parent, **base)

    c_ideal_var = StringVar(value=PLOT_SETTINGS.get("color_ideal", "#27ae60"))
    c_discard_var = StringVar(value=PLOT_SETTINGS.get("color_discard", "#c0392b"))
    c_axis_var = StringVar(value=PLOT_SETTINGS.get("axis_color", "#000000"))
    c_grid_var = StringVar(value=PLOT_SETTINGS.get("grid_color", "#e0e0e0"))
    c_bg_var = StringVar(value=PLOT_SETTINGS.get("plot_bg", "#ffffff"))

    font_size_var = IntVar(value=PLOT_SETTINGS.get("font_size", 12))
    font_size_bold_var = BooleanVar(value=PLOT_SETTINGS.get("font_bold", True))
    marker_size_var = IntVar(value=PLOT_SETTINGS.get("marker_size", 8))
    line_width_var = DoubleVar(value=PLOT_SETTINGS.get("line_width", 2.0))
    axis_width_var = DoubleVar(value=PLOT_SETTINGS.get("axis_width", 2.5))
    grid_width_var = DoubleVar(value=PLOT_SETTINGS.get("grid_width", 0.5))
    dist_style_var = StringVar(value=PLOT_SETTINGS.get("dist_style", "Bars"))
    show_gauss_var = BooleanVar(value=PLOT_SETTINGS.get("show_gaussian", False))
    dots_axis_var = BooleanVar(value=PLOT_SETTINGS.get("dots_axis_line", True))

    show_grid_var = BooleanVar(value=PLOT_SETTINGS.get("show_grid", True))
    show_legend_var = BooleanVar(value=PLOT_SETTINGS.get("show_legend", True))
    legend_pos_var = StringVar(value=PLOT_SETTINGS.get("legend_pos", "upper left"))
    n_factors_var = IntVar(value=PLOT_SETTINGS.get("n_factors", 5))
    dpi_var = IntVar(value=PLOT_SETTINGS.get("dpi", 300))

    def pick_color(var, swatch_widget):
        c = colorchooser.askcolor(initialcolor=var.get())[1]
        if c:
            var.set(c)
            try:
                swatch_widget.configure(bg=c)
            except Exception:
                pass

    FONT_TITLE = 12
    FONT_LABEL = 11
    FONT_SMALL = 10
    SLIDER_LEN = 260

    def section_title(text):
        tk.Label(scrollable, text=f"━━ {text} ━━", bg=CL["bg"], fg=CL["accent"], font=app._get_font(FONT_TITLE, True)).pack(pady=(8, 3), padx=10, anchor=W)

    def slider_row(label, var, from_, to, resolution=1):
        fr = tk.Frame(scrollable, bg=CL["bg"])
        fr.pack(fill=X, padx=10, pady=1)
        tk.Label(fr, text=label, bg=CL["bg"], fg=CL["fg"], font=app._get_font(FONT_LABEL)).pack(anchor=W)
        tk.Scale(
            fr,
            from_=from_,
            to=to,
            variable=var,
            orient=HORIZONTAL,
            resolution=resolution,
            bg=CL["bg3"],
            fg=CL["fg"],
            troughcolor=CL["accent"],
            length=SLIDER_LEN,
            highlightthickness=0,
        ).pack(anchor=W)

    def check_row(label, var):
        fr = tk.Frame(scrollable, bg=CL["bg"])
        fr.pack(fill=X, padx=10, pady=0)
        tk.Checkbutton(fr, text=label, variable=var, bg=CL["bg"], fg=CL["fg"], selectcolor=CL["bg2"], activebackground=CL["bg"], font=app._get_font(FONT_LABEL), highlightthickness=0).pack(anchor=W)

    def combo_row(label, var, values, width=25):
        fr = tk.Frame(scrollable, bg=CL["bg"])
        fr.pack(fill=X, padx=10, pady=1)
        tk.Label(fr, text=label, bg=CL["bg"], fg=CL["fg"], font=app._get_font(FONT_LABEL)).pack(anchor=W)
        ttk.Combobox(fr, textvariable=var, values=values, state="readonly", width=width, font=app._get_font(FONT_LABEL)).pack(anchor=W, pady=(1, 0))

    section_title(T["sec_colors"])
    fr_colors = tk.Frame(scrollable, bg=CL["bg"])
    fr_colors.pack(fill=X, padx=10, pady=0)
    for lbl_txt, var in [
        (T["ideal_points"], c_ideal_var),
        (T["discard_points"], c_discard_var),
        (T["axis_lines"], c_axis_var),
        (T["grid_lines"], c_grid_var),
        (T["plot_bg"], c_bg_var),
    ]:
        fr = tk.Frame(fr_colors, bg=CL["bg"])
        fr.pack(fill=X, pady=0)
        tk.Label(fr, text=lbl_txt, bg=CL["bg"], fg=CL["fg"], width=14, anchor=W, font=app._get_font(FONT_LABEL)).pack(side=LEFT)
        sw = tk.Canvas(fr, width=18, height=14, bg=var.get(), highlightthickness=1, highlightbackground=CL["border"])
        sw.pack(side=LEFT, padx=(6, 6), pady=1)
        sw.bind("<Button-1>", lambda e, v=var, s=sw: pick_color(v, s))
        tk.Label(fr, textvariable=var, bg=CL["bg"], fg=CL["dim"], width=9, anchor=W, font=app._get_font(FONT_SMALL)).pack(side=LEFT)

    section_title(T["sec_typo"])
    fr_font = tk.Frame(scrollable, bg=CL["bg"])
    fr_font.pack(fill=X, padx=10, pady=2)
    tk.Label(fr_font, text=T["font_size"], bg=CL["bg"], fg=CL["fg"], font=app._get_font(FONT_LABEL)).pack(anchor=W)
    tk.Scale(fr_font, from_=8, to=24, variable=font_size_var, orient=HORIZONTAL, bg=CL["bg3"], fg=CL["fg"], troughcolor=CL["accent"], length=SLIDER_LEN, highlightthickness=0).pack(anchor=W)
    check_row(T["bold_labels"], font_size_bold_var)

    section_title(T["sec_graphics"])
    slider_row(T["marker_size"], marker_size_var, 3, 20)
    slider_row(T["line_width"], line_width_var, 0.5, 5.0, 0.5)
    slider_row(T["axis_width"], axis_width_var, 1.0, 5.0, 0.5)
    slider_row(T["grid_width"], grid_width_var, 0.1, 2.0, 0.1)
    combo_row(T["dist_style"], dist_style_var, T["dist_styles"], width=18)
    check_row(T["gauss"], show_gauss_var)
    check_row(T["dots_axis"], dots_axis_var)
    check_row(T["show_grid"], show_grid_var)
    check_row(T["show_legend"], show_legend_var)
    combo_row(T["legend_pos"], legend_pos_var, T["legend_positions"], width=18)

    section_title(T["sec_axes"])
    tk.Label(scrollable, text=T["tick_factors"], bg=CL["bg"], fg=CL["fg"], font=app._get_font(FONT_LABEL)).pack(anchor=W, padx=10, pady=(3, 0))
    tk.Scale(scrollable, from_=3, to=12, variable=n_factors_var, orient=HORIZONTAL, bg=CL["bg3"], fg=CL["fg"], troughcolor=CL["accent"], length=SLIDER_LEN, highlightthickness=0).pack(anchor=W, padx=10)

    section_title(T["sec_export"])
    fr_dpi = tk.Frame(scrollable, bg=CL["bg"])
    fr_dpi.pack(fill=X, padx=10, pady=3)
    tk.Label(fr_dpi, text=T["export_dpi"], bg=CL["bg"], fg=CL["fg"], font=app._get_font(FONT_TITLE, True)).pack(anchor=W)
    dpi_label = tk.Label(fr_dpi, text=f"{dpi_var.get()} DPI", bg=CL["bg"], fg=CL["accent"], font=app._get_font(FONT_TITLE, True))
    tk.Scale(fr_dpi, from_=72, to=2400, variable=dpi_var, orient=HORIZONTAL, bg=CL["bg3"], fg=CL["fg"], troughcolor=CL["accent"], length=SLIDER_LEN, highlightthickness=0, command=lambda v: dpi_label.config(text=f"{v} DPI")).pack(anchor=W)
    dpi_label.pack(anchor=E)

    fr_presets = tk.Frame(fr_dpi, bg=CL["bg"])
    fr_presets.pack(fill=X, pady=2)
    tk.Label(fr_presets, text=T["quick_presets"], bg=CL["bg"], fg=CL["dim"], font=app._get_font(FONT_SMALL)).pack(anchor=W)
    for preset in [72, 150, 300, 600, 1200, 2400]:
        _themed_button(
            fr_presets,
            text=f"{preset}",
            width=4,
            height=1,
            bg=CL["accent"],
            activebackground=CL["accent2"],
            fg="#000000",
            activeforeground="#000000",
            command=lambda p=preset: (dpi_var.set(p), dpi_label.config(text=f"{p} DPI")),
        ).pack(side=LEFT, padx=1)
    pub_label = "Publication" if lang == "English" else "Publicación"
    _themed_button(
        fr_presets,
        text=pub_label,
        width=12,
        height=1,
        bg=CL["info"],
        activebackground="#2980b9",
        fg="#000000",
        activeforeground="#000000",
        command=lambda: (
            c_axis_var.set("#111111"),
            c_grid_var.set("#d0d0d0"),
            c_bg_var.set("#ffffff"),
            c_ideal_var.set("#1f77b4"),
            c_discard_var.set("#7f7f7f"),
            font_size_var.set(8),
            font_size_bold_var.set(False),
            axis_width_var.set(1.0),
            grid_width_var.set(0.3),
            show_grid_var.set(False),
            show_legend_var.set(True),
            legend_pos_var.set("upper right" if lang == "English" else "arriba derecha"),
            dpi_var.set(600),
            dpi_label.config(text="600 DPI"),
        ),
    ).pack(side=LEFT, padx=(8, 1))

    fr_buttons = tk.Frame(scrollable, bg=CL["bg"])
    fr_buttons.pack(fill=X, padx=10, pady=(10, 8))

    def apply_settings():
        PLOT_SETTINGS.update(
            {
                "color_ideal": c_ideal_var.get(),
                "color_discard": c_discard_var.get(),
                "axis_color": c_axis_var.get(),
                "grid_color": c_grid_var.get(),
                "plot_bg": c_bg_var.get(),
                "font_size": font_size_var.get(),
                "font_bold": font_size_bold_var.get(),
                "marker_size": marker_size_var.get(),
                "line_width": line_width_var.get(),
                "axis_width": axis_width_var.get(),
                "grid_width": grid_width_var.get(),
                "dist_style": (
                    "Bars"
                    if dist_style_var.get() in ("Bars", "Barras")
                    else "Dots"
                    if dist_style_var.get() in ("Dots", "Pelotas")
                    else "Box"
                    if dist_style_var.get() in ("Box", "Caja")
                    else "Bars"
                ),
                "show_gaussian": show_gauss_var.get(),
                "dots_axis_line": dots_axis_var.get(),
                "show_grid": show_grid_var.get(),
                "show_legend": show_legend_var.get(),
                "legend_pos": (
                    "upper left"
                    if legend_pos_var.get() in ("upper left", "arriba izquierda")
                    else "upper right"
                    if legend_pos_var.get() in ("upper right", "arriba derecha")
                    else "lower left"
                    if legend_pos_var.get() in ("lower left", "abajo izquierda")
                    else "lower right"
                    if legend_pos_var.get() in ("lower right", "abajo derecha")
                    else "center"
                    if legend_pos_var.get() in ("center", "centro")
                    else "upper left"
                ),
                "n_factors": n_factors_var.get(),
                "dpi": dpi_var.get(),
                "export_fig_w_in": float(PLOT_SETTINGS.get("export_fig_w_in", 3.35)),
                "export_fig_h_in": float(PLOT_SETTINGS.get("export_fig_h_in", 2.35)),
                "font_family": str(PLOT_SETTINGS.get("font_family", "DejaVu Sans")),
            }
        )
        app._draw_plots()
        top.destroy()

    _themed_button(
        fr_buttons,
        text=T["apply"],
        command=apply_settings,
        bg=CL["accent"],
        activebackground=CL["accent2"],
        fg="#000000",
        activeforeground="#000000",
        font=app._get_font(FONT_TITLE, True),
        height=1,
    ).pack(fill=X, pady=(1, 3))
    _themed_button(
        fr_buttons,
        text=T["cancel"],
        command=top.destroy,
        bg="#e0e0e0",
        activebackground="#cfcfcf",
        fg="#000000",
        activeforeground="#000000",
        font=app._get_font(FONT_LABEL),
        height=1,
    ).pack(fill=X)

