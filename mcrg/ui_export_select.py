from __future__ import annotations


def _display_label(row) -> str:
    candidate = str(row.get("Candidate_Name", "") or "").strip()
    smiles = str(row.get("SMILES_Final", "") or "").strip()
    if candidate and smiles:
        return f"{candidate} | {smiles}"
    return candidate or smiles or "Candidate"


def _clean_df(df):
    if df is None or getattr(df, "empty", True):
        return None
    try:
        out = df.copy()
    except Exception:
        return df
    subset = []
    if "SMILES_Final" in getattr(out, "columns", []):
        subset.append("SMILES_Final")
    elif "Candidate_Name" in getattr(out, "columns", []):
        subset.append("Candidate_Name")
    if subset:
        try:
            out = out.drop_duplicates(subset=subset, keep="first")
        except Exception:
            pass
    return out


def choose_export_dataframe(app, g: dict, *, title_key: str, ideal_df=None, manual_df=None):
    tk = g["tk"]
    messagebox = g["messagebox"]
    CL = g["CL"]
    HAS_CTK = g["HAS_CTK"]

    ideal_df = _clean_df(ideal_df)
    manual_df = _clean_df(manual_df)

    has_ideal = ideal_df is not None and not getattr(ideal_df, "empty", True)
    has_manual = manual_df is not None and not getattr(manual_df, "empty", True)

    if not has_ideal and not has_manual:
        messagebox.showinfo("!", app.t("export_select_need_candidates"))
        return None

    dlg = tk.Toplevel(app.root)
    dlg.title(app.t(title_key))
    dlg.transient(app.root)
    dlg.grab_set()
    dlg.resizable(False, False)
    dlg.configure(bg=CL["bg2"])

    container = tk.Frame(dlg, bg=CL["bg2"], padx=14, pady=14)
    container.pack(fill="both", expand=True)

    mode = tk.StringVar(value="ideal" if has_ideal else "manual")
    result = {"df": None}

    lbl_title = app._lbl(
        container,
        text=app.t(title_key),
        font=app._get_font(14, True),
        text_color=CL["accent"],
        fg_color=CL["bg2"] if HAS_CTK else None,
    )
    lbl_title.pack(anchor="w")

    lbl_hint = app._lbl(
        container,
        text=app.t("export_select_hint"),
        font=app._get_font(11),
        text_color=CL["dim"],
        fg_color=CL["bg2"] if HAS_CTK else None,
        wraplength=460,
        justify="left",
    )
    lbl_hint.pack(fill="x", pady=(6, 10))

    fr_modes = tk.Frame(container, bg=CL["bg2"])
    fr_modes.pack(fill="x", pady=(0, 8))

    rb_ideal = tk.Radiobutton(
        fr_modes,
        text=app.t("export_select_mode_ideal"),
        value="ideal",
        variable=mode,
        bg=CL["bg2"],
        fg=CL["fg"],
        selectcolor=CL["bg3"],
        activebackground=CL["bg2"],
        activeforeground=CL["fg"],
        font=app._get_font(11),
        anchor="w",
        state="normal" if has_ideal else "disabled",
        command=lambda: _sync_state(),
    )
    rb_ideal.pack(anchor="w")

    rb_manual = tk.Radiobutton(
        fr_modes,
        text=app.t("export_select_mode_manual"),
        value="manual",
        variable=mode,
        bg=CL["bg2"],
        fg=CL["fg"],
        selectcolor=CL["bg3"],
        activebackground=CL["bg2"],
        activeforeground=CL["fg"],
        font=app._get_font(11),
        anchor="w",
        state="normal" if has_manual else "disabled",
        command=lambda: _sync_state(),
    )
    rb_manual.pack(anchor="w", pady=(4, 0))

    lbl_candidates = app._lbl(
        container,
        text=app.t("export_select_candidates"),
        font=app._get_font(12, True),
        text_color=CL["fg"],
        fg_color=CL["bg2"] if HAS_CTK else None,
    )
    lbl_candidates.pack(anchor="w", pady=(8, 6))

    fr_list = tk.Frame(container, bg=CL["bg2"])
    fr_list.pack(fill="both", expand=True)

    listbox = tk.Listbox(
        fr_list,
        selectmode=tk.EXTENDED,
        exportselection=False,
        width=68,
        height=12,
        bg=CL["entry"],
        fg=CL["fg"],
        selectbackground=CL["accent"],
        selectforeground="#ffffff",
        highlightthickness=1,
        highlightbackground=CL["border"],
        relief="flat",
        font=app._get_font(11),
    )
    listbox.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(fr_list, orient="vertical", command=listbox.yview)
    scrollbar.pack(side="right", fill="y")
    listbox.configure(yscrollcommand=scrollbar.set)

    manual_labels = []
    if has_manual:
        try:
            for _, row in manual_df.iterrows():
                label = _display_label(row)
                manual_labels.append(label)
                listbox.insert("end", label)
        except Exception:
            pass

    fr_pick = tk.Frame(container, bg=CL["bg2"])
    fr_pick.pack(fill="x", pady=(8, 10))

    btn_all = app._btn(
        fr_pick,
        text=app.t("export_select_all"),
        width=110,
        height=30,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=lambda: _select_all(),
    )
    btn_all.pack(side="left")

    btn_clear = app._btn(
        fr_pick,
        text=app.t("export_select_clear"),
        width=110,
        height=30,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=lambda: listbox.selection_clear(0, "end"),
    )
    btn_clear.pack(side="left", padx=(8, 0))

    fr_actions = tk.Frame(container, bg=CL["bg2"])
    fr_actions.pack(fill="x")

    def _accept():
        if mode.get() == "ideal":
            if not has_ideal:
                messagebox.showinfo("!", app.t("export_select_need_candidates"))
                return
            result["df"] = ideal_df.copy() if hasattr(ideal_df, "copy") else ideal_df
            dlg.destroy()
            return

        if not has_manual:
            messagebox.showinfo("!", app.t("export_select_need_candidates"))
            return
        selected = list(listbox.curselection())
        if not selected:
            messagebox.showinfo("!", app.t("export_select_need_manual"))
            return
        try:
            result["df"] = manual_df.iloc[selected].copy()
        except Exception:
            result["df"] = manual_df
        dlg.destroy()

    btn_cancel = app._btn(
        fr_actions,
        text=app.t("export_select_cancel"),
        width=110,
        height=32,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=dlg.destroy,
    )
    btn_cancel.pack(side="right")

    btn_ok = app._btn(
        fr_actions,
        text=app.t("export_select_apply"),
        width=150,
        height=32,
        fg_color=CL["accent"],
        hover_color=CL["accent2"],
        text_color="#ffffff",
        font=app._get_font(11, True),
        command=_accept,
    )
    btn_ok.pack(side="right", padx=(0, 8))

    def _select_all():
        if str(mode.get()) != "manual":
            return
        listbox.selection_clear(0, "end")
        if manual_labels:
            listbox.selection_set(0, "end")

    def _sync_state():
        state = "normal" if str(mode.get()) == "manual" and has_manual else "disabled"
        try:
            listbox.configure(state=state)
            btn_all.configure(state=state) if HAS_CTK else btn_all.config(state=state)
            btn_clear.configure(state=state) if HAS_CTK else btn_clear.config(state=state)
        except Exception:
            pass

    _sync_state()
    try:
        dlg.update_idletasks()
        dlg.geometry(f"+{app.root.winfo_rootx()+120}+{app.root.winfo_rooty()+120}")
    except Exception:
        pass
    dlg.wait_window()
    return result.get("df")
