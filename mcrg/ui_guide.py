from __future__ import annotations


def build_guide(app, g: dict):
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
    WORD = g["WORD"]
    DISABLED = g["DISABLED"]

    fr = app.tab_frames["guide"]
    if HAS_CTK:
        scroll = ctk.CTkScrollableFrame(fr, fg_color=CL["bg"])
        scroll.pack(fill=BOTH, expand=True, padx=16, pady=12)
    else:
        canvas = tk.Canvas(fr, bg=CL["bg"], highlightthickness=0)
        sb = tk.Scrollbar(fr, orient=VERTICAL, command=canvas.yview)
        scroll = tk.Frame(canvas, bg=CL["bg"])
        scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        sb.pack(side=RIGHT, fill=Y)

    app.guide_text = tk.Text(
        scroll,
        height=28,
        wrap=WORD,
        font=("Helvetica", 15),
        bg=CL["bg"],
        fg=CL["fg"],
        insertbackground=CL["fg"],
        state=DISABLED,
        bd=0,
        padx=12,
        pady=8,
    )
    app.guide_text.pack(fill=BOTH, expand=True, padx=4, pady=(4, 2))
    app.guide_text.tag_configure("title", foreground=CL["accent"], font=("Helvetica", 16, "bold"))
    app.guide_text.tag_configure("subtitle", foreground=CL["info"], font=("Helvetica", 14, "bold"))
    app.guide_text.tag_configure("code", font=("Courier New", 13), foreground="#f1c40f")
    app.guide_text.tag_configure("warn", foreground="#e74c3c", font=("Helvetica", 13, "bold"))

    fr_btns = app._frame(scroll, fg_color=CL["bg2"] if HAS_CTK else None)
    fr_btns.pack(fill=X, padx=4, pady=(8, 10))

    def _guide_button_section(title: str, buttons: list[tuple[str, str, callable]], *, pady_top: int = 0):
        section = app._frame(fr_btns, fg_color=CL["bg2"] if HAS_CTK else None)
        section.pack(fill=X, padx=12, pady=(pady_top, 10))

        app._lbl(
            section,
            text=title,
            font=app._get_font(13, True),
            text_color=CL["fg"],
        ).pack(anchor="w", pady=(4, 6))

        row = app._frame(section, fg_color=CL["bg2"] if HAS_CTK else None)
        row.pack(fill=X)
        for col in range(3):
            try:
                row.grid_columnconfigure(col, weight=1, uniform="guide_btns")
            except Exception:
                pass

        for idx, (label, tone, command) in enumerate(buttons):
            btn = app._btn(
                row,
                text=label,
                width=170,
                height=34,
                fg_color=CL["accent"] if tone == "accent" else CL["bg3"],
                hover_color=CL["accent2"] if tone == "accent" else CL["border"],
                text_color="#fff" if tone == "accent" else CL["fg"],
                font=app._get_font(11),
                command=command,
            )
            btn.grid(row=0, column=idx, sticky="ew", padx=(0, 8) if idx < 2 else (0, 0), pady=(0, 2))

    _guide_button_section(
        app.t("guide_templates_title"),
        [
            (app.t("guide_template_csv"), "accent", lambda: app._download_example("csv")),
            (app.t("guide_template_txt"), "neutral", lambda: app._download_example("txt")),
            (app.t("guide_template_xlsx"), "neutral", lambda: app._download_example("xlsx")),
        ],
    )

    _guide_button_section(
        app.t("guide_packs_title"),
        [
            (app.t("guide_pack_biginelli"), "accent", lambda: app._download_example_pack("biginelli")),
            (app.t("guide_pack_gbb"), "neutral", lambda: app._download_example_pack("gbb")),
            (app.t("guide_pack_gewald"), "neutral", lambda: app._download_example_pack("gewald")),
        ],
        pady_top=2,
    )

