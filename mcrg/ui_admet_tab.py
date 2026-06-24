from __future__ import annotations

from .ui_exports_simple import choose_table_export_options, export_dataframe


def build_admet(app, g: dict):
    tk = g["tk"]
    ttk = g["ttk"]
    HAS_CTK = g["HAS_CTK"]
    ctk = g["ctk"]
    CL = g["CL"]
    X = g["X"]
    BOTH = g["BOTH"]
    LEFT = g["LEFT"]
    RIGHT = g["RIGHT"]
    Y = g["Y"]
    W = g["W"]
    END = g["END"]
    E = g["E"]

    def _card(parent):
        if HAS_CTK:
            return ctk.CTkFrame(parent, fg_color=CL["bg2"], corner_radius=12)
        return tk.Frame(parent, bg=CL["bg2"], highlightthickness=1, highlightbackground=CL["border"], bd=0)

    fr = app.tab_frames["admet"]

    root = app._frame(fr, fg_color=CL["bg"] if HAS_CTK else None)
    root.pack(fill=BOTH, expand=True, padx=16, pady=12)

    top = app._frame(root, fg_color=CL["bg"] if HAS_CTK else None)
    top.pack(fill=X, pady=(0, 10))
    app.lbl_admet_hint = app._lbl(top, text="", font=app._get_font(12), text_color=CL["dim"], wraplength=900, justify=LEFT)
    app.lbl_admet_hint.pack(fill=X, anchor=W)
    app.lbl_admet_runtime_status = app._lbl(top, text="Runtime status loading", font=app._get_font(11), text_color=CL["info"], wraplength=900, justify=LEFT)
    app.lbl_admet_runtime_status.pack(fill=X, anchor=W, pady=(6, 0))
    app.lbl_admet_perf_status = app._lbl(top, text="CPU: n/a | RAM: n/a | GPU: n/a", font=app._get_font(11), text_color=CL["dim"], wraplength=900, justify=LEFT)
    app.lbl_admet_perf_status.pack(fill=X, anchor=W, pady=(2, 0))

    app.lbl_admet_rstats = app._lbl(root, text="", font=app._get_font(12), text_color=CL["dim"])
    app.lbl_admet_rstats.pack(fill=X, pady=(0, 10))

    content = app._frame(root, fg_color=CL["bg"] if HAS_CTK else None)
    content.pack(fill=BOTH, expand=True)
    content.grid_columnconfigure(0, weight=1, uniform="admet_cols")
    content.grid_columnconfigure(1, weight=1, uniform="admet_cols")
    content.grid_rowconfigure(0, weight=3)
    content.grid_rowconfigure(1, weight=2)

    viewer_card = _card(content)
    outputs_card = _card(content)
    input_card = _card(content)
    info_card = _card(content)

    viewer_card.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
    outputs_card.grid(row=1, column=0, sticky="nsew", padx=(0, 8), pady=(8, 0))
    input_card.grid(row=0, column=1, sticky="nsew", padx=(8, 0), pady=(0, 8))
    info_card.grid(row=1, column=1, sticky="nsew", padx=(8, 0), pady=(8, 0))

    try:
        viewer_card.grid_rowconfigure(2, weight=1)
        viewer_card.grid_columnconfigure(0, weight=1)
        outputs_card.grid_rowconfigure(1, weight=1)
        outputs_card.grid_columnconfigure(0, weight=1)
        input_card.grid_rowconfigure(4, weight=1)
        input_card.grid_columnconfigure(0, weight=1)
        info_card.grid_rowconfigure(1, weight=1)
        info_card.grid_columnconfigure(0, weight=1)
    except Exception:
        pass

    app.lbl_admet_candidate_title = app._lbl(viewer_card, text="", font=app._get_font(17, True), text_color=CL["accent"])
    app.lbl_admet_candidate_title.pack(anchor=W, padx=16, pady=(14, 4))
    app.lbl_admet_candidate_smiles = app._lbl(viewer_card, text="", font=app._get_font(12), text_color=CL["dim"], wraplength=440, justify=LEFT)
    app.lbl_admet_candidate_smiles.pack(fill=X, anchor=W, padx=16, pady=(0, 10))
    viewer_body = app._frame(viewer_card, fg_color=CL["bg2"] if HAS_CTK else None)
    viewer_body.pack(fill=BOTH, expand=True, padx=16, pady=(0, 16))
    app.admet_canvas_2d = tk.Canvas(
        viewer_body,
        width=520,
        height=340,
        bg="#ffffff",
        highlightthickness=2,
        highlightbackground=CL["border"],
        bd=0,
        relief="flat",
    )
    app.admet_canvas_2d.pack(fill=BOTH, expand=True)

    app.lbl_admet_summary_title = app._lbl(outputs_card, text="", font=app._get_font(17, True), text_color=CL["accent"])
    app.lbl_admet_summary_title.pack(anchor=W, padx=16, pady=(14, 4))
    app.admet_summary = tk.Text(
        outputs_card,
        height=12,
        wrap="word",
        bg=CL["entry"],
        fg=CL["fg"],
        insertbackground=CL["fg"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=CL["border"],
        font=("Helvetica Neue", 12),
    )
    app.admet_summary.pack(fill=BOTH, expand=True, padx=16, pady=(0, 16))
    app.admet_summary.insert(END, app.t("admet_tab_summary_empty"))
    app.admet_summary.configure(state="disabled")

    app.lbl_admet_input_title = app._lbl(input_card, text="", font=app._get_font(17, True), text_color=CL["accent"])
    app.lbl_admet_input_title.pack(anchor=W, padx=16, pady=(14, 4))
    app.lbl_admet_input_hint = app._lbl(input_card, text="", font=app._get_font(12), text_color=CL["dim"], wraplength=440, justify=LEFT)
    app.lbl_admet_input_hint.pack(fill=X, anchor=W, padx=16, pady=(0, 10))

    fr_search = app._frame(input_card, fg_color=CL["bg2"] if HAS_CTK else None)
    fr_search.pack(fill=X, padx=16, pady=(0, 10))
    app.lbl_admet_search = app._lbl(fr_search, text="", font=app._get_font(13, True), text_color=CL["fg"])
    app.lbl_admet_search.pack(side=LEFT)

    app.combo_admet_search = ttk.Combobox(fr_search, textvariable=app.admet_search_var, values=[], width=36, font=app._get_font(12))
    app.combo_admet_search.pack(side=LEFT, fill=X, expand=True, padx=(10, 8))
    app.combo_admet_search.bind("<<ComboboxSelected>>", lambda e: app._apply_admet_filter())
    app.combo_admet_search.bind("<KeyRelease>", lambda e: app._apply_admet_filter())
    app.combo_admet_search.bind("<Return>", lambda e: app._apply_admet_filter())

    app.btn_admet_search_clear = app._btn(
        fr_search,
        text="",
        width=88,
        height=30,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(12),
        command=lambda: (_clear_admet_search(app), app._apply_admet_filter()),
    )
    app.btn_admet_search_clear.pack(side=RIGHT)

    fr_input = app._frame(input_card, fg_color=CL["bg2"] if HAS_CTK else None)
    fr_input.pack(fill=BOTH, expand=True, padx=16, pady=(0, 16))
    app.admet_input_text = tk.Text(
        fr_input,
        height=8,
        wrap="word",
        bg=CL["entry"],
        fg=CL["fg"],
        insertbackground=CL["fg"],
        relief="flat",
        highlightthickness=1,
        highlightbackground=CL["border"],
        font=("Helvetica Neue", 12),
    )
    app.admet_input_text.pack(fill=BOTH, expand=True, pady=(0, 12))

    fr_actions = app._frame(fr_input, fg_color=CL["bg2"] if HAS_CTK else None)
    fr_actions.pack(fill=X)
    for col in range(2):
        try:
            fr_actions.grid_columnconfigure(col, weight=1)
        except Exception:
            pass

    app.btn_admet_run_input = app._btn(
        fr_actions,
        text="",
        width=190,
        height=36,
        fg_color=CL["accent"],
        hover_color=CL["accent2"],
        text_color="#ffffff",
        font=app._get_font(12, True),
        command=lambda: app._admet_predict_pasted_local(app.admet_input_text.get("1.0", "end")),
    )
    app.btn_admet_run_input.grid(row=0, column=0, sticky="ew", padx=(0, 6), pady=(0, 8))

    app.btn_admet_use_ideal = app._btn(
        fr_actions,
        text="",
        width=190,
        height=34,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(12),
        command=app._admet_predict_results_local,
    )
    app.btn_admet_use_ideal.grid(row=0, column=1, sticky="ew", padx=(6, 0), pady=(0, 8))

    app.btn_admet_export_zip = None

    app.btn_admet_export_csv_tab = app._btn(
        fr_actions,
        text="",
        width=190,
        height=34,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(12),
        command=app._export_admet_csv,
    )
    app.btn_admet_export_csv_tab.grid(row=1, column=0, columnspan=2, sticky="ew", padx=(0, 0), pady=(0, 8))

    info_header = app._frame(info_card, fg_color=CL["bg2"] if HAS_CTK else None)
    info_header.pack(fill=X, padx=16, pady=(14, 8))
    app.lbl_admet_info_title = app._lbl(info_header, text="", font=app._get_font(17, True), text_color=CL["accent"])
    app.lbl_admet_info_title.pack(anchor=W)
    app.lbl_admet_info_hint = app._lbl(info_header, text="", font=app._get_font(12), text_color=CL["dim"], wraplength=440, justify=LEFT)
    app.lbl_admet_info_hint.pack(fill=X, anchor=W, pady=(4, 0))

    app._admet_help_panels = []

    def _make_panel(title_key: str, body_key: str, default_visible: bool = True):
        state = {"visible": bool(default_visible)}
        fr_panel = tk.Frame(info_card, bg=CL["bg2"])
        fr_panel.pack(fill=X, padx=16, pady=(0, 10))

        btn = app._btn(
            fr_panel,
            text="",
            width=320,
            height=30,
            fg_color=CL["bg3"],
            hover_color=CL["border"],
            text_color=CL["fg"],
            font=app._get_font(13, True),
            command=lambda: _toggle(),
        )
        btn.pack(fill=X)

        fr_body = tk.Frame(fr_panel, bg=CL["bg2"])
        fr_body.pack(fill=BOTH, expand=False, pady=(6, 0))

        txt = tk.Text(
            fr_body,
            height=9,
            wrap="word",
            bg=CL["entry"],
            fg=CL["fg"],
            insertbackground=CL["fg"],
            relief="flat",
            highlightthickness=1,
            highlightbackground=CL["border"],
            font=("Helvetica Neue", 12),
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
            prefix = "▾ " if state.get("visible", True) else "▸ "
            try:
                btn.configure(text=prefix + app.t(title_key)) if HAS_CTK else btn.config(text=prefix + app.t(title_key))
            except Exception:
                pass

        if not state["visible"]:
            fr_body.pack_forget()

        app._admet_help_panels.append(
            {
                "title_key": title_key,
                "body_key": body_key,
                "btn": btn,
                "state": state,
                "set_text": set_text,
            }
        )

    _make_panel("admet_help_input_title", "admet_help_input", default_visible=True)
    _make_panel("admet_help_outputs_title", "admet_help_outputs", default_visible=False)
    _make_panel("admet_help_workflow_title", "admet_help_workflow", default_visible=False)

    _clear_admet_search(app)
    clear_admet_view(app, g)


def _clear_admet_search(app):
    try:
        app.admet_search_var.set("")
    except Exception:
        pass


def _display_label(row) -> str:
    candidate = str(row.get("Candidate_Name", "") or "").strip()
    smiles = str(row.get("SMILES_Final", "") or "").strip()
    if candidate and smiles:
        return f"{candidate} | {smiles}"
    return smiles or candidate or "Candidate"


def _display_values(df) -> list[str]:
    if df is None or getattr(df, "empty", True):
        return []
    values = []
    seen = set()
    try:
        for _, row in df.iterrows():
            label = _display_label(row)
            if label not in seen:
                seen.add(label)
                values.append(label)
    except Exception:
        return []
    return values


def _summary_text(app, row, empty_text: str) -> str:
    base_cols = {
        "Candidate_Name",
        "SMILES_Final",
        "Classification",
        "Compatibility_%",
        "Failure_Reason",
        "Ideal_Rule",
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
        "Has_Stereo",
        "Chiral_Centers",
        "Chiral_Centers_Defined",
        "Chiral_Centers_Unassigned",
        "Chiral_Tags",
        "InChIKey",
    }
    lines = []
    for col, value in row.items():
        if col in base_cols:
            continue
        text = str(value).strip()
        if not text:
            continue
        lines.append(f"{app._col_label(col)}: {text}")
    return "\n".join(lines) if lines else empty_text


def _show_row(app, g: dict, row):
    CENTER = g["CENTER"]
    HAS_CTK = g["HAS_CTK"]
    mol_to_photoimage = g["mol_to_photoimage"]

    candidate = str(row.get("Candidate_Name", "") or "").strip() or "Candidate"
    smiles = str(row.get("SMILES_Final", "") or "").strip()
    app.admet_active_smiles = smiles

    title = app.t("admet_tab_candidate_title", candidate=candidate)
    summary_title = app.t("admet_tab_summary_title", candidate=candidate)
    smiles_line = app.t("admet_tab_candidate_smiles", smiles=smiles or "—")
    (app.lbl_admet_candidate_title.configure(text=title) if HAS_CTK else app.lbl_admet_candidate_title.config(text=title))
    (app.lbl_admet_candidate_smiles.configure(text=smiles_line) if HAS_CTK else app.lbl_admet_candidate_smiles.config(text=smiles_line))
    (app.lbl_admet_summary_title.configure(text=summary_title) if HAS_CTK else app.lbl_admet_summary_title.config(text=summary_title))

    app.admet_canvas_2d.delete("all")
    img, err = mol_to_photoimage(smiles, (460, 300))
    if img:
        app._admet_mol_img_ref = img
        try:
            cx = int(app.admet_canvas_2d.winfo_width() / 2)
            cy = int(app.admet_canvas_2d.winfo_height() / 2)
        except Exception:
            cx, cy = 240, 160
        app.admet_canvas_2d.create_image(cx, cy, image=img)
    else:
        app._admet_mol_img_ref = None
        msg = f"2D render unavailable\n\n{err}"
        try:
            cx = int(app.admet_canvas_2d.winfo_width() / 2)
            cy = int(app.admet_canvas_2d.winfo_height() / 2)
        except Exception:
            cx, cy = 240, 160
        app.admet_canvas_2d.create_text(cx, cy, text=msg, fill="#888", font=app._get_font(13), justify=CENTER)

    try:
        app.admet_summary.configure(state="normal")
        app.admet_summary.delete("1.0", "end")
        app.admet_summary.insert("1.0", _summary_text(app, row, app.t("admet_tab_summary_empty")))
        app.admet_summary.configure(state="disabled")
    except Exception:
        pass


def _clear_admet_detail_widgets(app, g: dict, *, keep_hint: bool):
    CENTER = g["CENTER"]
    HAS_CTK = g["HAS_CTK"]

    app.admet_active_smiles = ""
    try:
        title = app.t("admet_tab_candidate_title_empty")
        summary_title = app.t("admet_tab_summary_title_empty")
        (app.lbl_admet_candidate_title.configure(text=title) if HAS_CTK else app.lbl_admet_candidate_title.config(text=title))
        (app.lbl_admet_candidate_smiles.configure(text="") if HAS_CTK else app.lbl_admet_candidate_smiles.config(text=""))
        (app.lbl_admet_summary_title.configure(text=summary_title) if HAS_CTK else app.lbl_admet_summary_title.config(text=summary_title))
    except Exception:
        pass
    try:
        app.admet_canvas_2d.delete("all")
        msg = app.t("admet_tab_no_predictions") if keep_hint else app.t("admet_tab_select_candidate")
        app.admet_canvas_2d.create_text(240, 160, text=msg, fill="#888", font=app._get_font(13), justify=CENTER)
    except Exception:
        pass
    try:
        app.admet_summary.configure(state="normal")
        app.admet_summary.delete("1.0", "end")
        app.admet_summary.insert("1.0", app.t("admet_tab_summary_empty"))
        app.admet_summary.configure(state="disabled")
    except Exception:
        pass


def apply_admet_filter(app, g: dict):
    HAS_CTK = g["HAS_CTK"]

    if not hasattr(app, "combo_admet_search"):
        return

    df = getattr(app, "df_admet_all", None)
    query = ""
    try:
        query = str(app.admet_search_var.get() or "").strip().lower()
    except Exception:
        query = ""

    if df is None or getattr(df, "empty", True):
        app.df_admet_view = df
        try:
            app.combo_admet_search.configure(values=[])
        except Exception:
            pass
        txt = app.t("admet_tab_no_predictions")
        (app.lbl_admet_rstats.configure(text=txt) if HAS_CTK else app.lbl_admet_rstats.config(text=txt))
        _clear_admet_detail_widgets(app, g, keep_hint=True)
        return

    try:
        app.combo_admet_search.configure(values=_display_values(df))
    except Exception:
        pass

    if query:
        mask = None
        cols = [c for c in ("Candidate_Name", "SMILES_Final", "Classification", "Failure_Reason") if c in getattr(df, "columns", [])]
        for col in cols:
            part = df[col].astype(str).str.lower().str.contains(query, regex=False, na=False)
            mask = part if mask is None else (mask | part)
        label_series = df.apply(lambda row: _display_label(row).lower(), axis=1)
        label_match = label_series.str.contains(query, regex=False, na=False)
        mask = label_match if mask is None else (mask | label_match)
        df_view = df.loc[mask].copy() if mask is not None else df.copy()
    else:
        df_view = df.copy()

    app.df_admet_view = df_view
    txt = app.t("admet_tab_results_count", n=len(df_view), total=len(df))
    (app.lbl_admet_rstats.configure(text=txt) if HAS_CTK else app.lbl_admet_rstats.config(text=txt))

    if getattr(df_view, "empty", True):
        _clear_admet_detail_widgets(app, g, keep_hint=False)
        return

    row = None
    active_smiles = str(getattr(app, "admet_active_smiles", "") or "").strip()
    if active_smiles and "SMILES_Final" in df_view.columns:
        current = df_view[df_view["SMILES_Final"].astype(str) == active_smiles]
        if not getattr(current, "empty", True):
            row = current.iloc[0]
    if row is None:
        row = df_view.iloc[0]
    _show_row(app, g, row)


def sort_admet_tree(app, g: dict, col: str):
    return None


def on_admet_select(app, g: dict, event):
    return None


def refresh_admet_labels(app, g: dict):
    HAS_CTK = g["HAS_CTK"]

    def _set_attr(name, **kw):
        w = getattr(app, name, None)
        if w and hasattr(w, "configure"):
            w.configure(**kw) if HAS_CTK else w.config(**kw)

    _set_attr("lbl_admet_hint", text=app.t("admet_tab_hint"))
    _set_attr("lbl_admet_input_title", text=app.t("admet_tab_input_title"))
    _set_attr("lbl_admet_input_hint", text=app.t("admet_tab_input_hint"))
    _set_attr("lbl_admet_info_title", text=app.t("admet_info_title"))
    _set_attr("lbl_admet_info_hint", text=app.t("admet_info_hint"))
    _set_attr("btn_admet_run_input", text=app.t("admet_tab_run_input"))
    _set_attr("btn_admet_use_ideal", text=app.t("admet_tab_use_results"))
    _set_attr("btn_admet_export_zip", text=app.t("exportar_zip"))
    _set_attr("lbl_admet_search", text=app.t("admet_tab_search"))
    _set_attr("btn_admet_search_clear", text=app.t("admet_tab_search_clear"))
    _set_attr("btn_admet_export_csv_tab", text=app.t("admet_export"))

    for p in getattr(app, "_admet_help_panels", []):
        try:
            prefix = "▾ " if p.get("state", {}).get("visible", True) else "▸ "
            btn = p.get("btn")
            if btn:
                (btn.configure(text=prefix + app.t(p.get("title_key"))) if HAS_CTK else btn.config(text=prefix + app.t(p.get("title_key"))))
            set_text = p.get("set_text")
            if callable(set_text):
                set_text()
        except Exception:
            continue

    if getattr(app, "df_admet_all", None) is None or getattr(app.df_admet_all, "empty", True):
        txt = app.t("admet_tab_no_predictions")
        _set_attr("lbl_admet_rstats", text=txt)
        _clear_admet_detail_widgets(app, g, keep_hint=True)
        return

    try:
        app._apply_admet_filter()
    except Exception:
        pass


def clear_admet_view(app, g: dict):
    HAS_CTK = g["HAS_CTK"]
    app.df_admet_all = None
    app.df_admet_view = None
    app._admet_mol_img_ref = None
    app.admet_active_smiles = ""
    _clear_admet_search(app)
    try:
        if hasattr(app, "combo_admet_search"):
            app.combo_admet_search.configure(values=[])
    except Exception:
        pass
    txt = app.t("admet_tab_no_predictions")
    try:
        (app.lbl_admet_rstats.configure(text=txt) if HAS_CTK else app.lbl_admet_rstats.config(text=txt))
    except Exception:
        pass
    _clear_admet_detail_widgets(app, g, keep_hint=True)


def export_admet_csv(app, g: dict):
    messagebox = g["messagebox"]

    df = getattr(app, "df_admet_all", None)
    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("admet_tab_no_predictions"))
        return
    opts = choose_table_export_options(
        app,
        g,
        title_key="admet_export_title",
        hint_key="admet_export_hint",
        df_all=df,
        formats=("csv", "xlsx", "pdf") if bool(getattr(app, "features", {}).get("export_pdf", False)) else ("csv", "xlsx"),
    )
    if not opts:
        return
    export_dataframe(
        app,
        g,
        opts["df"],
        opts["format"],
        initial_prefix=f"moleku_admet_{str(opts['scope']).lower()}",
    )
