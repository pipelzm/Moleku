from __future__ import annotations


def build_results(app, g: dict):
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
    E = g["E"]
    W = g["W"]

    fr = app.tab_frames["resultados"]
    ff = app._frame(fr, fg_color=CL["bg"] if HAS_CTK else None)
    ff.pack(fill=X, padx=16, pady=(12, 6))
    app.lbl_filt = app._lbl(ff, text="", font=app._get_font(12, True), text_color=CL["fg"])
    app.lbl_filt.pack(side=LEFT)

    app.btn_table_custom = app._btn(
        ff,
        text=app.t("table_view_custom"),
        width=120,
        height=28,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=app._show_table_columns_dialog,
    )
    app.btn_table_custom.pack(side=LEFT, padx=(12, 8))
    app._rbs = []
    if HAS_CTK:
        app.seg_filter = ctk.CTkSegmentedButton(
            ff,
            values=["Ideal", "All", "Discard"],
            command=lambda v: (app.filter_var.set(v), app._apply_filter()),
            font=app._get_font(12),
            selected_color=CL["accent"],
            unselected_color=CL["bg3"],
        )
        app.seg_filter.set("Ideal")
        app.seg_filter.pack(side=LEFT, padx=8)
    else:
        for v in ("Ideal", "All", "Discard"):
            rb = tk.Radiobutton(
                ff,
                text=v,
                variable=app.filter_var,
                value=v,
                bg=CL["bg"],
                fg=CL["fg"],
                selectcolor=CL["bg2"],
                activebackground=CL["bg"],
                font=app._get_font(12),
                command=app._apply_filter,
            )
            rb.pack(side=LEFT, padx=6)
            app._rbs.append((v, rb))

    app.btn_clear_res = app._btn(
        ff,
        text=app.t("limpiar_todo"),
        width=120,
        height=28,
        fg_color=CL["discard"],
        hover_color="#a93226",
        text_color="#fff",
        font=app._get_font(11),
        command=app._clear_results,
    )
    app.btn_clear_res.pack(side=RIGHT, padx=2)
    app.btn_restart = app._btn(
        ff,
        text=app.t("reiniciar"),
        width=100,
        height=28,
        fg_color=CL["info"],
        hover_color="#2980b9",
        text_color="#fff",
        font=app._get_font(11),
        command=app._restart_app,
    )
    app.btn_restart.pack(side=RIGHT, padx=2)

    app.btn_admet_open = app._btn(
        ff,
        text="",
        width=160,
        height=28,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=app._admet_open_web,
    )
    app.btn_admet_open.pack(side=RIGHT, padx=2)
    app.lbl_rstats = app._lbl(fr, text="", font=app._get_font(12), text_color=CL["dim"])
    app.lbl_rstats.pack(fill=X, padx=16)

    ft = tk.Frame(fr, bg=CL["bg"])
    ft.pack(fill=BOTH, expand=True, padx=16, pady=(4, 4))
    # Initial columns are reaction-aware; apply_filter will later align them to df columns.
    try:
        mcr_key = app.mcr_var.get()
        comps = list(g["MCR_CATALOGO"].get(mcr_key, {}).get("componentes", []))
    except Exception:
        comps = []
    comp_smiles_cols = [f"{c}_SMILES" for c in comps]
    cols = tuple(
        [
            "Compatibility_%",
            "Classification",
            "Failure_Reason",
            "SMILES_Final",
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
        ]
        + comps
        + comp_smiles_cols
        + [
            "Molecular_Weight",
            "LogP",
            "TPSA",
            "HBA",
            "HBD",
            "QED",
            "Fsp3",
            "Rotatable_Bonds",
            "Heavy_Atoms",
            "Ring_Count",
            "Molar_Refractivity",
            "PAINS_Alerts",
            "Brenk_Alerts",
            "Pass_Lipinski",
            "Pass_Ghose",
            "Pass_Veber",
            "Pass_Egan",
            "Pass_Muegge",
        ]
    )
    style = ttk.Style()
    style.theme_use("default")
    style.configure("T.Treeview", background=CL["bg2"], foreground=CL["fg"], fieldbackground=CL["bg2"], rowheight=28, font=("Helvetica Neue", 10))
    style.configure("T.Treeview.Heading", background=CL["bg3"], foreground=CL["accent"], font=app._get_font(12, True), relief="flat")
    style.map("T.Treeview", background=[("selected", CL["accent"])], foreground=[("selected", "#fff")])
    app.tree = ttk.Treeview(ft, columns=cols, show="headings", selectmode="extended", style="T.Treeview")
    for c in cols:
        app.tree.heading(c, text=app._col_label(c), command=lambda _c=c: app._sort(_c))
        app.tree.column(c, width=120 if c in ("Compatibility_%", "Core_Reagent", "Classification") else 90, minwidth=50)
    vs = ttk.Scrollbar(ft, orient=VERTICAL, command=app.tree.yview)
    hs = ttk.Scrollbar(ft, orient=HORIZONTAL, command=app.tree.xview)
    app.tree.configure(yscrollcommand=vs.set, xscrollcommand=hs.set)
    app.tree.grid(row=0, column=0, sticky="nsew")
    vs.grid(row=0, column=1, sticky="ns")
    hs.grid(row=1, column=0, sticky="ew")
    ft.rowconfigure(0, weight=1)
    ft.columnconfigure(0, weight=1)
    app.tree.bind("<<TreeviewSelect>>", app._on_tree_select)

    fr_table_actions = app._frame(fr, fg_color=CL["bg"] if HAS_CTK else None)
    fr_table_actions.pack(fill=X, padx=16, pady=(2, 6))

    # v1.0 core exports: CSV + XLSX.
    # PDF export is kept behind a feature gate (future pack / when fully stable).
    export_btns = [("exportar_csv", app._exp_csv), ("exportar_xlsx", app._exp_xlsx)]
    if bool(getattr(app, "features", {}).get("export_pdf", False)):
        export_btns.append(("exportar_pdf", app._exp_pdf))
    for txt, cmd in export_btns:
        b = app._btn(
            fr_table_actions,
            text="",
            width=130,
            height=32,
            corner_radius=6,
            fg_color=CL["bg3"],
            hover_color=CL["border"],
            text_color=CL["fg"],
            font=app._get_font(11),
            command=cmd,
        )
        b.pack(side=LEFT, padx=(0, 6))
        setattr(app, f"btn_{txt}", b)
    app.btn_exportar_zip = None

    # Custom ZIP is intentionally not part of the v1.0 core.
    if bool(getattr(app, "features", {}).get("custom_zip", False)):
        app.btn_exportar_custom_zip = app._btn(
            fr_table_actions,
            text=app.t("exportar_custom_zip"),
            width=120,
            height=32,
            corner_radius=6,
            fg_color=CL["bg3"],
            hover_color=CL["border"],
            text_color=CL["fg"],
            font=app._get_font(11),
            command=app._show_custom_zip_dialog,
        )
        app.btn_exportar_custom_zip.pack(side=LEFT, padx=(6, 6))
    else:
        app.btn_exportar_custom_zip = None

    app.btn_admet_copy_sel = app._btn(
        fr_table_actions,
        text="",
        width=170,
        height=32,
        corner_radius=6,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=app._admet_copy_selected_smiles,
    )
    app.btn_admet_copy_sel.pack(side=LEFT, padx=(10, 6))
    app.btn_admet_copy_ideal = app._btn(
        fr_table_actions,
        text="",
        width=150,
        height=32,
        corner_radius=6,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=app._admet_copy_ideal_smiles,
    )
    app.btn_admet_copy_ideal.pack(side=LEFT, padx=(0, 6))

    app.btn_admet_predict = app._btn(
        fr_table_actions,
        text="",
        width=140,
        height=32,
        corner_radius=6,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=app._admet_predict_selected_local,
    )
    # v1.0 keeps ADMET local available (optional dependency). Can be moved to a future pack.
    if bool(getattr(app, "features", {}).get("admet_local", True)):
        app.btn_admet_predict.pack(side=LEFT, padx=(10, 6))
    else:
        try:
            app.btn_admet_predict.configure(state="disabled") if HAS_CTK else app.btn_admet_predict.config(state="disabled")
        except Exception:
            pass

    fr_bot = app._frame(fr, fg_color=CL["bg"] if HAS_CTK else None)
    fr_bot.pack(fill=X, padx=16, pady=(2, 4))
    app.lbl_2d_title = app._lbl(fr_bot, text="", font=app._get_font(15, True), text_color=CL["accent"])
    if not HAS_CTK:
        app.lbl_2d_title.config(fg=CL["accent"])
    app.lbl_2d_title.pack(anchor=W)

    app.results_info_visible = True
    app.btn_toggle_results_info = app._btn(
        fr_bot,
        text=app.t("results_toggle_info_hide"),
        width=170,
        height=26,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(12, True),
        command=app._toggle_results_info_panels,
    )
    app.btn_toggle_results_info.pack(anchor=E, pady=(2, 0))
    fr_2d_row = app._frame(fr_bot, fg_color=CL["bg"] if HAS_CTK else None)
    fr_2d_row.pack(fill=X, pady=4)
    app._canvas_2d_compact_w = 280
    app._canvas_2d_expanded_w = 560
    app.canvas_2d = tk.Canvas(fr_2d_row, width=app._canvas_2d_compact_w, height=220, bg="#ffffff", highlightthickness=2, highlightbackground=CL["border"])
    app.canvas_2d.pack(side=LEFT, padx=(0, 12))
    app.fr_stats = app._frame(fr_2d_row, fg_color=CL["bg"] if HAS_CTK else None)
    app.fr_stats.pack(side=LEFT, fill=Y)
    app.stat_labels = {}
    for key in (
        "stats_score",
        "stats_mw",
        "stats_logp",
        "stats_tpsa",
        "stats_hba",
        "stats_hbd",
        "stats_qed",
        "stats_fsp3",
        "stats_rb",
        "stats_rings",
        "stats_heavy",
        "stats_mr",
        "stats_pains",
        "stats_brenk",
        # Chirality / stereochemistry summary
        "stats_has_stereo",
        "stats_chiral_centers",
    ):
        lbl = app._lbl(app.fr_stats, text="", font=app._get_font(14), text_color=CL["fg"])
        if not HAS_CTK:
            lbl.config(fg=CL["fg"])
        lbl.pack(anchor=W, pady=4)
        app.stat_labels[key] = lbl

    # The collapsible help panels are built inside app._refresh_results_help_panels,
    # so we only need the container frames that layout toggles depend on.
    app.fr_param_help = app._frame(fr_2d_row, fg_color=CL["bg"] if HAS_CTK else None)
    app.fr_param_help.pack(side=RIGHT, fill=Y, padx=(12, 0))

    # ── Collapsible information panels (Results) ───────────────────────
    # These texts already exist in i18n as:
    # - results_help_params(_title)
    # - results_help_workflow(_title)
    # - results_help_views(_title)
    #
    # We build them once here and later only refresh their labels/texts
    # via app._refresh_results_help_panels().
    try:
        app._results_help_panels = []

        def _make_panel(title_key: str, body_key: str, default_visible: bool = True):
            state = {"visible": bool(default_visible)}

            fr_panel = tk.Frame(app.fr_param_help, bg=CL["bg"])
            fr_panel.pack(fill=X, pady=(0, 10))

            btn = app._btn(
                fr_panel,
                text="",
                width=260,
                height=28,
                fg_color=CL["bg3"],
                hover_color=CL["border"],
                text_color=CL["fg"],
                font=app._get_font(12, True),
                command=lambda: _toggle(),
            )
            btn.pack(fill=X)

            fr_body = tk.Frame(fr_panel, bg=CL["bg"])
            fr_body.pack(fill=BOTH, expand=False, pady=(6, 0))

            txt = tk.Text(
                fr_body,
                height=9,
                wrap="word",
                bg=CL["bg2"],
                fg=CL["fg"],
                insertbackground=CL["fg"],
                relief="flat",
                highlightthickness=1,
                highlightbackground=CL["border"],
            )
            txt.pack(fill=BOTH, expand=True)
            txt.configure(state="disabled")

            def set_text():
                try:
                    txt.configure(state="normal")
                    txt.delete("1.0", "end")
                    txt.insert("1.0", app.t(body_key))
                    txt.configure(state="disabled")
                except Exception:
                    try:
                        txt.configure(state="disabled")
                    except Exception:
                        pass

            def _toggle():
                state["visible"] = not state.get("visible", True)
                if state["visible"]:
                    if not fr_body.winfo_ismapped():
                        fr_body.pack(fill=BOTH, expand=False, pady=(6, 0))
                else:
                    if fr_body.winfo_ismapped():
                        fr_body.pack_forget()
                # Update the header arrow + localized title
                try:
                    prefix = "▾ " if state.get("visible", True) else "▸ "
                    btn.configure(text=prefix + app.t(title_key)) if HAS_CTK else btn.config(text=prefix + app.t(title_key))
                except Exception:
                    pass

            # Initial visibility
            if not state["visible"]:
                fr_body.pack_forget()

            app._results_help_panels.append(
                {
                    "title_key": title_key,
                    "body_key": body_key,
                    "btn": btn,
                    "state": state,
                    "set_text": set_text,
                }
            )

        _make_panel("results_help_params_title", "results_help_params", default_visible=True)
        _make_panel("results_help_workflow_title", "results_help_workflow", default_visible=False)
        _make_panel("results_help_views_title", "results_help_views", default_visible=False)

        # Ensure initial localized titles/texts and correct visibility arrows.
        app._refresh_results_help_panels()
    except Exception:
        # Never fail the Results tab if help panels cannot be built.
        app._results_help_panels = getattr(app, "_results_help_panels", [])

    # Ensure the initial layout matches the current toggle state.
    try:
        app._apply_results_info_layout()
    except Exception:
        pass

