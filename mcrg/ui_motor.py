from __future__ import annotations


def build_motor(app, g: dict):
    tk = g["tk"]
    ttk = g["ttk"]
    ctk = g.get("ctk")
    HAS_CTK = g["HAS_CTK"]
    CL = g["CL"]
    X = g["X"]
    Y = g["Y"]
    BOTH = g["BOTH"]
    LEFT = g["LEFT"]
    RIGHT = g["RIGHT"]
    VERTICAL = g["VERTICAL"]
    HORIZONTAL = g["HORIZONTAL"]
    FLAT = g["FLAT"]
    PREVIEW_CANVAS_HEIGHT = g["PREVIEW_CANVAS_HEIGHT"]
    MCR_CATALOGO = g["MCR_CATALOGO"]
    StringVar = g["StringVar"]
    BooleanVar = g["BooleanVar"]
    W = g["W"]
    END = g["END"]
    NORMAL = g["NORMAL"]
    DISABLED = g["DISABLED"]

    fr = app.tab_frames["motor"]
    if HAS_CTK:
        scroll = ctk.CTkScrollableFrame(fr, fg_color=CL["bg"])
        scroll.pack(fill=BOTH, expand=True)
    else:
        canvas = tk.Canvas(fr, bg=CL["bg"], highlightthickness=0)
        sb = tk.Scrollbar(fr, orient=VERTICAL, command=canvas.yview)
        scroll = tk.Frame(canvas, bg=CL["bg"])
        scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        sb.pack(side=RIGHT, fill=Y)

    inner = scroll
    px = 16
    bn = ctk.CTkFrame(inner, fg_color=CL["bg3"], corner_radius=6) if HAS_CTK else tk.Frame(inner, bg=CL["bg3"])
    bn.pack(fill=X, padx=px, pady=(12, 6))
    app.lbl_info = app._lbl(bn, text="", font=app._get_font(13), text_color=CL["info"], fg_color=CL["bg3"] if HAS_CTK else None)
    if not HAS_CTK:
        app.lbl_info.config(fg=CL["info"], bg=CL["bg3"])
    app.lbl_info.pack(fill=X, padx=12, pady=8)

    fr_mcr = app._frame(inner, fg_color=CL["bg"] if HAS_CTK else None)
    fr_mcr.pack(fill=X, padx=px, pady=(4, 6))
    app._lbl(fr_mcr, text=app.t("mcr_label"), font=app._get_font(13, True), text_color=CL["fg"]).pack(side=LEFT)
    if HAS_CTK:
        app.combo_mcr = ctk.CTkComboBox(
            fr_mcr,
            variable=app.mcr_var,
            values=list(MCR_CATALOGO.keys()),
            width=320,
            font=app._get_font(13),
            command=lambda v: (app._refresh_slots(), app._update_preview()),
        )
    else:
        app.combo_mcr = ttk.Combobox(
            fr_mcr,
            textvariable=app.mcr_var,
            values=list(MCR_CATALOGO.keys()),
            state="readonly",
            font=app._get_font(13),
            width=38,
        )
        app.combo_mcr.bind("<<ComboboxSelected>>", lambda e: (app._refresh_slots(), app._update_preview()))
    app.combo_mcr.pack(side=LEFT, padx=8)

    preview_fr = app._frame(inner, fg_color=CL["plot_bg"] if HAS_CTK else None)
    preview_fr.pack(fill=X, padx=px, pady=(4, 8))
    app._lbl(preview_fr, text=app.t("data_preview"), font=app._get_font(15, True), text_color=CL["plot_fg"] if HAS_CTK else None).pack(pady=(8, 2))
    app.preview_canvas = tk.Canvas(preview_fr, height=PREVIEW_CANVAS_HEIGHT, bg="#ffffff", highlightthickness=2, highlightbackground=CL["border"])
    app.preview_canvas.pack(fill=X, padx=10, pady=(0, 8))
    app.preview_canvas.bind("<Configure>", lambda e: app._schedule_preview_redraw())
    app.lbl_preview_desc = app._lbl(preview_fr, text="", font=app._get_font(13), text_color="#333333" if HAS_CTK else None, wraplength=700, justify=LEFT)
    if not HAS_CTK:
        app.lbl_preview_desc.config(fg="#333333", bg="#ffffff")
    app.lbl_preview_desc.pack(fill=X, padx=15, pady=(0, 4))
    app.lbl_preview_doi = app._lbl(preview_fr, text="", font=app._get_font(11, True), text_color="#666666", justify="center")
    if not HAS_CTK:
        app.lbl_preview_doi.config(fg="#666666", bg="#ffffff")
    app.lbl_preview_doi.pack(pady=(0, 8))

    app.fr_slots = app._frame(inner, fg_color=CL["bg"] if HAS_CTK else None)
    app.fr_slots.pack(fill=X, padx=px, pady=(2, 4))
    app.fr_central = (
        ctk.CTkFrame(inner, fg_color=CL["bg2"], corner_radius=6, border_width=1, border_color=CL["border"])
        if HAS_CTK
        else tk.LabelFrame(inner, text="", bg=CL["bg"], fg=CL["fg"])
    )
    app.fr_central.pack(fill=X, padx=px, pady=(2, 4))
    app.fr_central_in = app._frame(app.fr_central, fg_color=CL["bg2"] if HAS_CTK else None)
    app.fr_central_in.pack(fill=X, padx=8, pady=6)

    fr_t = app._frame(inner, fg_color=CL["bg"] if HAS_CTK else None)
    fr_t.pack(fill=X, padx=px, pady=(6, 4))
    app.lbl_thr_t = app._lbl(fr_t, text="", font=app._get_font(13, True), text_color=CL["fg"])
    app.lbl_thr_t.pack(side=LEFT)
    app.lbl_thr_v = app._lbl(fr_t, text=f"{app.threshold_var.get():.1f}", font=app._get_font(13, True), text_color=CL["accent"], width=50)
    if not HAS_CTK:
        app.lbl_thr_v.config(fg=CL["accent"])
    app.lbl_thr_v.pack(side=RIGHT)
    if HAS_CTK:
        app.slider = ctk.CTkSlider(
            fr_t,
            from_=0,
            to=100,
            variable=app.threshold_var,
            progress_color=CL["accent"],
            button_color=CL["fg"],
            button_hover_color=CL["accent2"],
            command=lambda v: app.lbl_thr_v.configure(text=f"{v:.1f}"),
        )
    else:
        app.slider = tk.Scale(
            fr_t,
            from_=0,
            to=100,
            orient=HORIZONTAL,
            resolution=0.5,
            variable=app.threshold_var,
            showvalue=False,
            length=300,
            bg=CL["bg"],
            fg=CL["fg"],
            troughcolor=CL["accent"],
            activebackground=CL["accent2"],
            highlightthickness=0,
            command=lambda v: app.lbl_thr_v.config(text=f"{float(v):.1f}"),
        )
    app.slider.pack(side=LEFT, fill=X, expand=True, padx=(12, 8))

    app.lbl_threshold_hint = app._lbl(
        inner,
        text=app.t("threshold_hint"),
        font=app._get_font(10),
        text_color=CL["dim"],
        wraplength=640,
        justify=LEFT,
    )
    app.lbl_threshold_hint.pack(fill=X, padx=px, pady=(0, 8))

    fr_rule = app._frame(inner, fg_color=CL["bg"] if HAS_CTK else None)
    fr_rule.pack(fill=X, padx=px, pady=(0, 6))
    app.lbl_ideal_rule = app._lbl(fr_rule, text=app.t("ideal_rule"), font=app._get_font(12, True), text_color=CL["fg"])
    app.lbl_ideal_rule.pack(side=LEFT)
    rule_opts = ["Lipinski", "Ghose", "Veber", "Egan", "Muegge", "Any", "All"]
    if HAS_CTK:
        app.combo_ideal_rule = ctk.CTkComboBox(fr_rule, variable=app.ideal_rule_var, values=rule_opts, width=160, font=app._get_font(11))
    else:
        app.combo_ideal_rule = ttk.Combobox(fr_rule, textvariable=app.ideal_rule_var, values=rule_opts, state="readonly", width=18, font=app._get_font(11))
    app.combo_ideal_rule.pack(side=LEFT, padx=8)

    app.lbl_ideal_rule_hint = app._lbl(
        inner,
        text=app.t("ideal_rule_hint"),
        font=app._get_font(10),
        text_color=CL["dim"],
        wraplength=640,
        justify=LEFT,
    )
    app.lbl_ideal_rule_hint.pack(fill=X, padx=px, pady=(0, 8))

    fr_std = app._frame(inner, fg_color=CL["bg"] if HAS_CTK else None)
    fr_std.pack(fill=X, padx=px, pady=(0, 6))
    if HAS_CTK:
        ctk.CTkCheckBox(fr_std, text=app.t("standardize"), variable=app.standardize_var, font=app._get_font(11), text_color=CL["fg"]).pack(anchor=W)
    else:
        tk.Checkbutton(
            fr_std,
            text=app.t("standardize"),
            variable=app.standardize_var,
            bg=CL["bg"],
            fg=CL["fg"],
            selectcolor=CL["bg2"],
            activebackground=CL["bg"],
            font=app._get_font(11),
            anchor="w",
            justify="left",
        ).pack(anchor=W)

    app.btn_start = app._btn(inner, text="", font=app._get_font(16, True), fg_color=CL["accent"], hover_color=CL["accent2"], text_color="#ffffff", height=44, corner_radius=8, command=app._run)
    app.btn_start.pack(fill=X, padx=px, pady=(10, 4))
    app.btn_clear = app._btn(inner, text="", font=app._get_font(13), fg_color=CL["bg3"], hover_color=CL["border"], text_color=CL["dim"], height=32, corner_radius=6, command=app._clear_motor_inputs)
    app.btn_clear.pack(fill=X, padx=px, pady=(2, 6))

    app.lbl_status = app._lbl(inner, text="", font=app._get_font(12), text_color=CL["info"])
    app.lbl_status.pack(fill=X, padx=px, pady=(4, 2))

    if HAS_CTK:
        app.pbar = ctk.CTkProgressBar(inner, progress_color=CL["accent"], fg_color=CL["bg3"])
    else:
        app.pbar = ttk.Progressbar(inner, orient=HORIZONTAL, mode="determinate", length=400)
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProgressbar", background=CL["accent"], troughcolor=CL["bg3"], bordercolor=CL["border"], lightcolor=CL["accent"], darkcolor=CL["accent2"])
    app.pbar.pack(fill=X, padx=px, pady=(0, 2))
    try:
        if HAS_CTK:
            app.pbar.set(0.0)
        else:
            app.pbar["value"] = 0
    except Exception:
        pass

    app.lbl_combinations = app._lbl(inner, text="📊 Total: 0 | ✅ Ideal: 0 | ❌ Discarded: 0", font=app._get_font(12), text_color=CL["dim"])
    app.lbl_combinations.pack(fill=X, padx=px, pady=(2, 4))

    app.console = tk.Text(inner, height=8, wrap="none", font=("Menlo", 12), bg=CL["bg3"], fg=CL["dim"], insertbackground=CL["fg"], state=DISABLED, bd=0, padx=10, pady=6)
    app.console.pack(fill=X, padx=px, pady=(4, 14))
    app._refresh_slots()

