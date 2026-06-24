from __future__ import annotations


RESULT_SCOPES = ("Ideal", "Warning", "Error", "Generated", "All")


def _norm_scope(scope: str) -> str:
    value = str(scope or "All").strip().lower()
    aliases = {
        "ideal": "Ideal",
        "warning": "Warning",
        "warn": "Warning",
        "error": "Error",
        "discard": "Error",
        "discarded": "Error",
        "generated": "Generated",
        "all": "All",
        "todos": "All",
    }
    return aliases.get(value, "All")


def filter_df_by_scope(df, scope: str):
    """Return rows matching a user-facing result scope."""
    scope = _norm_scope(scope)
    if df is None or getattr(df, "empty", True):
        return df

    try:
        out = df.copy()
    except Exception:
        out = df

    cols = list(getattr(out, "columns", []))
    if scope == "All":
        return out

    smiles_mask = None
    if "SMILES_Final" in cols:
        try:
            smiles_mask = out["SMILES_Final"].fillna("").astype(str).str.strip().str.len() > 0
        except Exception:
            smiles_mask = None

    if scope == "Generated":
        if smiles_mask is None:
            return out
        return out.loc[smiles_mask].copy()

    if "Review_Status" in cols:
        try:
            return out.loc[out["Review_Status"].fillna("").astype(str).str.lower() == scope.lower()].copy()
        except Exception:
            pass

    if "Classification" in cols:
        try:
            cls = out["Classification"].fillna("").astype(str)
            if scope == "Ideal":
                return out.loc[cls == "Ideal"].copy()
            if scope == "Warning":
                if smiles_mask is not None:
                    return out.loc[(cls != "Ideal") & smiles_mask].copy()
                return out.loc[cls != "Ideal"].copy()
            if scope == "Error":
                if smiles_mask is not None:
                    return out.loc[(cls != "Ideal") & (~smiles_mask)].copy()
                return out.loc[cls != "Ideal"].copy()
        except Exception:
            pass

    return out.iloc[0:0].copy() if hasattr(out, "iloc") else out


def get_filtered_df(app):
    """Return the dataframe matching the current Results-table filter.

    The Results tab exposes Ideal / Warning / Error / Generated / All. This
    helper preserves old direct export methods while the UI now uses the
    consolidated Export Table dialog.
    """
    try:
        v = app.filter_var.get() if hasattr(app, "filter_var") else "All"
    except Exception:
        v = "All"
    return filter_df_by_scope(getattr(app, "df_all", None), v)


def _filter_suffix(app) -> str:
    """Return a short filename-friendly suffix for the active filter."""
    try:
        v = app.filter_var.get() if hasattr(app, "filter_var") else "All"
    except Exception:
        v = "All"
    return _norm_scope(v).lower()


def _scope_label(app, scope: str) -> str:
    key = {
        "Ideal": "ideal",
        "Warning": "warning",
        "Error": "error",
        "Generated": "generated",
        "All": "todos",
    }.get(_norm_scope(scope), "todos")
    return app.t(key)


def choose_table_export_options(app, g: dict, *, title_key: str, hint_key: str, df_all, scopes=None, formats=None):
    tk = g["tk"]
    messagebox = g["messagebox"]
    CL = g["CL"]
    HAS_CTK = g["HAS_CTK"]

    if df_all is None or getattr(df_all, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return None

    scopes = tuple(scopes or RESULT_SCOPES)
    formats = tuple(formats or ("csv", "xlsx", "pdf"))
    scoped = {}
    for scope in scopes:
        key = _norm_scope(scope)
        scoped[key] = filter_df_by_scope(df_all, key)

    available_scopes = [s for s in scopes if scoped.get(_norm_scope(s)) is not None and not getattr(scoped.get(_norm_scope(s)), "empty", True)]
    if not available_scopes:
        messagebox.showinfo("!", app.t("no_datos"))
        return None

    default_scope = _norm_scope("Generated" if _norm_scope("Generated") in [_norm_scope(s) for s in available_scopes] else available_scopes[0])
    scope_var = tk.StringVar(value=default_scope)
    fmt_var = tk.StringVar(value=formats[0] if formats else "csv")
    result = {"scope": None, "format": None, "df": None}

    dlg = tk.Toplevel(app.root)
    dlg.title(app.t(title_key))
    dlg.transient(app.root)
    dlg.grab_set()
    dlg.resizable(False, False)
    dlg.configure(bg=CL["bg2"])

    container = tk.Frame(dlg, bg=CL["bg2"], padx=14, pady=14)
    container.pack(fill="both", expand=True)

    app._lbl(
        container,
        text=app.t(title_key),
        font=app._get_font(14, True),
        text_color=CL["accent"],
        fg_color=CL["bg2"] if HAS_CTK else None,
    ).pack(anchor="w")
    app._lbl(
        container,
        text=app.t(hint_key),
        font=app._get_font(11),
        text_color=CL["dim"],
        fg_color=CL["bg2"] if HAS_CTK else None,
        wraplength=460,
        justify="left",
    ).pack(fill="x", pady=(6, 12))

    fr_scope = tk.LabelFrame(
        container,
        text=app.t("export_scope"),
        bg=CL["bg2"],
        fg=CL["fg"],
        bd=1,
        relief="solid",
        font=app._get_font(11, True),
        padx=10,
        pady=8,
    )
    fr_scope.pack(fill="x", pady=(0, 10))

    for scope in scopes:
        key = _norm_scope(scope)
        df_scope = scoped.get(key)
        count = 0 if df_scope is None or getattr(df_scope, "empty", True) else int(len(df_scope))
        rb = tk.Radiobutton(
            fr_scope,
            text=f"{_scope_label(app, key)} ({count})",
            value=key,
            variable=scope_var,
            bg=CL["bg2"],
            fg=CL["fg"],
            selectcolor=CL["bg3"],
            activebackground=CL["bg2"],
            activeforeground=CL["fg"],
            font=app._get_font(11),
            anchor="w",
            state="normal" if count else "disabled",
        )
        rb.pack(anchor="w", pady=(0, 3))

    fr_fmt = tk.LabelFrame(
        container,
        text=app.t("export_format"),
        bg=CL["bg2"],
        fg=CL["fg"],
        bd=1,
        relief="solid",
        font=app._get_font(11, True),
        padx=10,
        pady=8,
    )
    fr_fmt.pack(fill="x", pady=(0, 12))

    fmt_labels = {
        "csv": app.t("export_format_csv"),
        "xlsx": app.t("export_format_xlsx"),
        "pdf": app.t("export_format_pdf"),
    }
    for fmt in formats:
        rb = tk.Radiobutton(
            fr_fmt,
            text=fmt_labels.get(fmt, fmt.upper()),
            value=fmt,
            variable=fmt_var,
            bg=CL["bg2"],
            fg=CL["fg"],
            selectcolor=CL["bg3"],
            activebackground=CL["bg2"],
            activeforeground=CL["fg"],
            font=app._get_font(11),
            anchor="w",
        )
        rb.pack(anchor="w", pady=(0, 3))

    fr_actions = tk.Frame(container, bg=CL["bg2"])
    fr_actions.pack(fill="x")

    def _accept():
        scope = _norm_scope(scope_var.get())
        df_scope = scoped.get(scope)
        if df_scope is None or getattr(df_scope, "empty", True):
            messagebox.showinfo("!", app.t("export_scope_empty"))
            return
        result["scope"] = scope
        result["format"] = str(fmt_var.get() or "csv")
        result["df"] = df_scope.copy() if hasattr(df_scope, "copy") else df_scope
        dlg.destroy()

    app._btn(
        fr_actions,
        text=app.t("export_select_cancel"),
        width=110,
        height=32,
        fg_color=CL["bg3"],
        hover_color=CL["border"],
        text_color=CL["fg"],
        font=app._get_font(11),
        command=dlg.destroy,
    ).pack(side="right")
    app._btn(
        fr_actions,
        text=app.t("export_select_apply"),
        width=150,
        height=32,
        fg_color=CL["accent"],
        hover_color=CL["accent2"],
        text_color="#ffffff",
        font=app._get_font(11, True),
        command=_accept,
    ).pack(side="right", padx=(0, 8))

    try:
        dlg.update_idletasks()
        dlg.geometry(f"+{app.root.winfo_rootx()+120}+{app.root.winfo_rooty()+120}")
    except Exception:
        pass
    dlg.wait_window()
    if result.get("df") is None:
        return None
    return result


def export_dataframe(app, g: dict, df, fmt: str, *, initial_prefix: str):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]

    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return

    fmt = str(fmt or "csv").lower()
    if fmt == "xlsx":
        ext = "xlsx"
        filetypes = [("Sheets", "*.xlsx")]
    elif fmt == "pdf":
        ext = "pdf"
        filetypes = [("PDF", "*.pdf")]
    else:
        ext = "csv"
        filetypes = [("CSV", "*.csv")]

    fp = filedialog.asksaveasfilename(
        defaultextension=f".{ext}",
        filetypes=filetypes,
        initialfile=f"{initial_prefix}.{ext}",
    )
    if not fp:
        return
    if fmt == "xlsx":
        df.to_excel(fp, index=False, engine="openpyxl")
    elif fmt == "pdf":
        app._export_pdf(df, fp)
        return
    else:
        df.to_csv(fp, index=False)
    messagebox.showinfo("OK", f"{app.t('saved')} {fp}")


def exp_table(app, g: dict):
    opts = choose_table_export_options(
        app,
        g,
        title_key="export_table_title",
        hint_key="export_table_hint",
        df_all=getattr(app, "df_all", None),
        formats=("csv", "xlsx", "pdf") if bool(getattr(app, "features", {}).get("export_pdf", False)) else ("csv", "xlsx"),
    )
    if not opts:
        return
    export_dataframe(
        app,
        g,
        opts["df"],
        opts["format"],
        initial_prefix=f"mcrg_results_{_norm_scope(opts['scope']).lower()}",
    )


def export_file(app, g: dict, ext: str, save_fn):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]

    df = get_filtered_df(app)
    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return
    initialfile = f"mcrg_results_{_filter_suffix(app)}.{ext}"
    fp = filedialog.asksaveasfilename(
        defaultextension=f".{ext}",
        filetypes=[(ext.upper(), f"*.{ext}")],
        initialfile=initialfile,
    )
    if fp:
        save_fn(df, fp)
        messagebox.showinfo("OK", f"{app.t('saved')} {fp}")


def exp_csv(app, g: dict):
    return export_file(app, g, "csv", lambda df, fp: df.to_csv(fp, index=False))


def exp_xlsx(app, g: dict):
    return export_file(app, g, "xlsx", lambda df, fp: df.to_excel(fp, index=False, engine="openpyxl"))


def exp_pdf(app, g: dict):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]

    df = get_filtered_df(app)
    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return
    initialfile = f"mcrg_results_{_filter_suffix(app)}.pdf"
    fp = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")],
        initialfile=initialfile,
    )
    if not fp:
        return
    app._export_pdf(df, fp)
