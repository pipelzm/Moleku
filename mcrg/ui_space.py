from __future__ import annotations


def build_space(app, g: dict):
    tk = g["tk"]
    ttk = g["ttk"]
    ctk = g.get("ctk")
    HAS_CTK = g["HAS_CTK"]
    CL = g["CL"]
    X = g["X"]
    BOTH = g["BOTH"]
    LEFT = g["LEFT"]
    RIGHT = g["RIGHT"]
    CENTER = g["CENTER"]
    StringVar = g["StringVar"]
    PLOT_DESC = g["PLOT_DESC"]

    fr = app.tab_frames["espacio"]
    fh = app._frame(fr, fg_color=CL["bg"] if HAS_CTK else None)
    fh.pack(fill=X, padx=16, pady=(12, 4))
    app.lbl_esp_t = app._lbl(fh, text="", font=app._get_font(16, True), text_color=CL["accent"])
    if not HAS_CTK:
        app.lbl_esp_t.config(fg=CL["accent"])
    app.lbl_esp_t.pack(side=LEFT)
    app.lbl_plot_sel = app._lbl(fh, text="", font=app._get_font(11), text_color=CL["dim"])
    if not HAS_CTK:
        app.lbl_plot_sel.config(fg=CL["dim"])
    app.lbl_plot_sel.pack(side=LEFT, padx=(16, 4))

    app._plot_keys = [k for k in PLOT_DESC.keys()]
    plot_opts = [app.t(p) for p in app._plot_keys]

    if HAS_CTK:
        app.combo_plot = ctk.CTkComboBox(fh, variable=app.plot_var, values=plot_opts, width=200, command=lambda v: app._render_espacio())
    else:
        app.combo_plot = ttk.Combobox(fh, textvariable=app.plot_var, values=plot_opts, state="readonly", width=24, font=app._get_font(11))
        app.combo_plot.bind("<<ComboboxSelected>>", lambda e: app._render_espacio())
    app.combo_plot.pack(side=LEFT, padx=4)

    app.lbl_versus = app._lbl(fh, text="Versus Mode:", font=app._get_font(11), text_color=CL["dim"])
    if not HAS_CTK:
        app.lbl_versus.config(fg=CL["dim"])
    app.lbl_versus.pack(side=LEFT, padx=(16, 4))

    app.versus_var = StringVar(value="Off")
    app.versus_plot_var = StringVar(value="")

    if HAS_CTK:
        app.combo_versus = ctk.CTkComboBox(fh, variable=app.versus_var, values=["Off"] + plot_opts, width=180, command=lambda v: app._render_espacio())
    else:
        app.combo_versus = ttk.Combobox(fh, textvariable=app.versus_var, values=["Off"] + plot_opts, state="readonly", width=20, font=app._get_font(11))
        app.combo_versus.bind("<<ComboboxSelected>>", lambda e: app._render_espacio())
    app.combo_versus.pack(side=LEFT, padx=4)

    app.lbl_versus_hint = None

    app.btn_export_plot = app._btn(
        fh,
        text=app.t("exportar_alta_calidad"),
        width=180,
        height=28,
        fg_color=CL["accent"],
        hover_color=CL["accent2"],
        text_color="#ffffff",
        font=app._get_font(11, True),
        command=app._export_plots_dialog,
    )
    app.btn_export_plot.pack(side=RIGHT, padx=4)
    app.btn_plot_settings = app._btn(
        fh,
        text="⚙ Plot Settings",
        width=100,
        height=28,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=app._show_plot_settings,
    )
    app.btn_plot_settings.pack(side=RIGHT, padx=4)

    app.plot_scroll_frame = app._frame(fr, fg_color=CL["bg"] if HAS_CTK else None)
    app.plot_scroll_frame.pack(fill=BOTH, expand=True, padx=16, pady=(8, 12))
    app.plot_canvas = tk.Canvas(app.plot_scroll_frame, bg=CL["bg"], highlightthickness=0)
    app.plot_scrollbar = ttk.Scrollbar(app.plot_scroll_frame, orient="vertical", command=app.plot_canvas.yview)
    app.plot_inner_frame = tk.Frame(app.plot_canvas, bg=CL["bg"])
    app.plot_inner_frame.bind("<Configure>", lambda e: app.plot_canvas.configure(scrollregion=app.plot_canvas.bbox("all")))
    app.plot_canvas.create_window((0, 0), window=app.plot_inner_frame, anchor="nw")
    app.plot_canvas.configure(yscrollcommand=app.plot_scrollbar.set)
    app.plot_canvas.pack(side="left", fill="both", expand=True)
    app.plot_scrollbar.pack(side="right", fill="y")
    app.lbl_plot_desc = app._lbl(fr, text="", font=app._get_font(13), text_color=CL["dim"], wraplength=800, justify=CENTER)
    if not HAS_CTK:
        app.lbl_plot_desc.config(fg=CL["dim"], bg=CL["bg"])
    app.lbl_plot_desc.pack(fill=X, padx=30, pady=(0, 8))
    app._render_espacio()

