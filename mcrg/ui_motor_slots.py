from __future__ import annotations

from .run_counts import format_run_counter


def refresh_slots(app, g: dict):
    tk = g["tk"]
    ctk = g.get("ctk")
    HAS_CTK = g["HAS_CTK"]
    CL = g["CL"]
    X = g["X"]
    LEFT = g["LEFT"]
    RIGHT = g["RIGHT"]
    W = g["W"]
    BooleanVar = g["BooleanVar"]
    StringVar = g["StringVar"]
    MCR_CATALOGO = g["MCR_CATALOGO"]
    display_component_name = g["display_component_name"]
    display_core_reagent_name = g["display_core_reagent_name"]
    FLAT = g["FLAT"]

    for w in app.fr_slots.winfo_children():
        w.destroy()
    app._file_slot_widgets = []
    mcr = app.mcr_var.get()
    if mcr not in MCR_CATALOGO:
        return
    componentes = MCR_CATALOGO[mcr]["componentes"]
    lang = app.lang_var.get()
    for comp in componentes:
        fr_comp = app._frame(app.fr_slots, fg_color=CL["bg2"] if HAS_CTK else None)
        fr_comp.pack(fill=X, padx=0, pady=(0, 6))
        disp = display_component_name(comp, lang)
        app._lbl(fr_comp, text=f"{disp}:", font=app._get_font(12, True), text_color=CL["accent"]).pack(side=LEFT, padx=12, pady=8)
        if comp not in app.file_svars:
            app.file_svars[comp] = StringVar()
        ent = tk.Entry(fr_comp, textvariable=app.file_svars[comp], bg=CL["entry"], fg=CL["fg"], insertbackground=CL["fg"], font=app._get_font(11), relief=FLAT, bd=0)
        ent.pack(side=LEFT, fill=X, expand=True, padx=(0, 8), pady=8)
        app._btn(fr_comp, text="Browser", width=110, height=30, fg_color=CL["accent"], hover_color=CL["accent2"], text_color="#fff", font=app._get_font(11), command=lambda c=comp: app._browse_file(c)).pack(side=RIGHT, padx=8, pady=4)
        app._file_slot_widgets.append((comp, fr_comp, ent))

    for w in app.fr_central_in.winfo_children():
        w.destroy()
    app.central_vars = {}
    app.lbl_core_selection = None
    opts = MCR_CATALOGO[mcr].get("opciones_centrales", {})
    if opts:
        # Localized header + hints for core reagents section
        title = app.t("reactivos_centrales") + " (" + app.t("core_reagents_select_hint") + "):"
        app._lbl(app.fr_central_in, text=title, font=app._get_font(12, True), text_color=CL["fg"]).pack(anchor=W, pady=(0, 6))

        app.lbl_core_selection = app._lbl(app.fr_central_in, text="", font=app._get_font(11, True), text_color=CL["info"], wraplength=520, justify=LEFT)
        if not HAS_CTK:
            app.lbl_core_selection.config(fg=CL["info"])
        app.lbl_core_selection.pack(anchor=W, pady=(0, 6), padx=5)

        def _update_core_selection_label():
            selected = [name for name, var in app.central_vars.items() if var.get()]
            if not app.lbl_core_selection:
                return
            if selected:
                lang2 = app.lang_var.get()
                disp2 = [display_core_reagent_name(n, lang2) for n in selected]
                txt = app.t("core_reagents_selected") + ": " + ", ".join(disp2)
            else:
                txt = app.t("core_reagents_selected") + ": " + app.t("core_reagents_selected_none")
            (app.lbl_core_selection.configure(text=txt) if HAS_CTK else app.lbl_core_selection.config(text=txt))

        for name in opts:
            if name not in app.central_vars:
                app.central_vars[name] = BooleanVar(value=False)
            lang2 = app.lang_var.get()
            disp_name = display_core_reagent_name(name, lang2)
            if HAS_CTK:
                cb = ctk.CTkCheckBox(app.fr_central_in, text=disp_name, variable=app.central_vars[name], font=app._get_font(12), text_color=CL["fg"], command=_update_core_selection_label)
            else:
                cb = tk.Checkbutton(app.fr_central_in, text=disp_name, variable=app.central_vars[name], bg=CL["bg"], fg=CL["fg"], selectcolor=CL["bg2"], activebackground=CL["bg"], font=app._get_font(12), anchor="w", justify="left", command=_update_core_selection_label)
            cb.pack(anchor=W, pady=2, padx=5)
        hint = "💡 " + app.t("core_reagents_tip")
        app._lbl(app.fr_central_in, text=hint, font=app._get_font(10), text_color=CL["dim"], wraplength=500).pack(anchor=W, pady=(8, 2))
        _update_core_selection_label()


def clear_motor_inputs(app, g: dict):
    HAS_CTK = g["HAS_CTK"]
    NORMAL = g["NORMAL"]
    DISABLED = g["DISABLED"]
    END = g["END"]

    try:
        app.file_paths = {}
        for sv in getattr(app, "file_svars", {}).values():
            sv.set("")
    except Exception:
        pass

    try:
        for v in getattr(app, "central_vars", {}).values():
            v.set(False)
    except Exception:
        pass

    try:
        if HAS_CTK:
            try:
                app.pbar.set(0)
            except Exception:
                pass
            app.lbl_status.configure(text="")
            app.lbl_combinations.configure(text=format_run_counter(None, None))
        else:
            try:
                app.pbar["value"] = 0
            except Exception:
                pass
            app.lbl_status.config(text="")
            app.lbl_combinations.config(text=format_run_counter(None, None))
    except Exception:
        pass

    try:
        app.console.config(state=NORMAL)
        app.console.delete("1.0", END)
        app.console.config(state=DISABLED)
    except Exception:
        pass

    app._refresh_slots()


def browse_file(app, g: dict, component: str):
    filedialog = g["filedialog"]
    fp = filedialog.askopenfilename(
        title=f"Select file for {component}",
        filetypes=[
            ("CSV/Text", "*.csv *.txt *.tsv *.smi"),
            ("Sheets", "*.xlsx *.xls *.ods"),
            ("JSON", "*.json"),
            ("Numbers", "*.numbers"),
            ("All", "*.*"),
        ],
    )
    if fp:
        app.file_paths[component] = fp
        app.file_svars[component].set(fp)
