from __future__ import annotations


def apply_filter(app, g: dict):
    END = g["END"]
    HAS_CTK = g["HAS_CTK"]
    PLOT_SETTINGS = g["PLOT_SETTINGS"]

    for r in app.tree.get_children():
        app.tree.delete(r)
    v = app.filter_var.get()
    if v == "Ideal":
        df = app.df_ideal
    elif v == "Discard":
        df = app.df_all[app.df_all["Classification"] != "Ideal"] if app.df_all is not None else None
    else:
        df = app.df_all

    core_cols = [
        "Compatibility_%",
        "Classification",
        "Failure_Reason",
        "SMILES_Final",
        # Chirality/stereo (v1.0)
        "Has_Stereo",
        "Chiral_Centers",
        "Chiral_Centers_Defined",
        "Chiral_Centers_Unassigned",
        "Chiral_Tags",
        "InChIKey",
        "Is_Duplicate",
        "Core_Reagent",
        "Ideal_Rule",
    ]

    custom_mode = bool(app._custom_table_cols)
    base_cols = list(app._custom_table_cols or core_cols)

    # Ensure the table adapts to the currently selected reaction, even before running.
    try:
        MCR_CATALOGO = g.get("MCR_CATALOGO", {})
        mcr_key = app.mcr_var.get() if hasattr(app, "mcr_var") else ""
        comps = list(MCR_CATALOGO.get(mcr_key, {}).get("componentes", []))
        comp_smiles_cols = [f"{c}_SMILES" for c in comps]
        reaction_cols = comps + comp_smiles_cols
        if not custom_mode:
            for c in reaction_cols:
                if c not in base_cols:
                    base_cols.append(c)
    except Exception:
        pass
    if df is None or getattr(df, "empty", True):
        cols = base_cols
        if getattr(app, "lbl_rstats", None):
            (app.lbl_rstats.configure(text=app.t("no_datos")) if HAS_CTK else app.lbl_rstats.config(text=app.t("no_datos")))
    else:
        st = f"{len(df)} {app.t('registros')}"
        (app.lbl_rstats.configure(text=st) if HAS_CTK else app.lbl_rstats.config(text=st))
        df_cols = list(df.columns)
        if custom_mode:
            cols = [c for c in base_cols if c in df_cols]
        else:
            cols = [c for c in base_cols if c in df_cols] + [c for c in df_cols if c not in base_cols]

    if tuple(cols) != tuple(app.tree["columns"]):
        app.tree["columns"] = cols
        for c in cols:
            app.tree.heading(c, text=app._col_label(c), command=lambda _c=c: app._sort(_c))
            w = 140 if c in ("SMILES_Final",) else (160 if c == "Failure_Reason" else (120 if c in ("Compatibility_%", "Core_Reagent", "Classification") else 100))
            app.tree.column(c, width=w, minwidth=60)
    if df is None or getattr(df, "empty", True):
        return

    for _, row in df.iterrows():
        tag = "ideal" if row.get("Classification") == "Ideal" else "desc"
        app.tree.insert("", END, values=[str(row.get(c, "")) for c in cols], tags=(tag,))
    app.tree.tag_configure("ideal", foreground=PLOT_SETTINGS["color_ideal"])
    app.tree.tag_configure("desc", foreground=PLOT_SETTINGS["color_discard"])
    app._update_results_counter()


def sort_tree(app, g: dict, col: str):
    data = [(app.tree.set(k, col), k) for k in app.tree.get_children("")]
    try:
        data.sort(key=lambda x: float(x[0]), reverse=True)
    except ValueError:
        data.sort(key=lambda x: x[0])
    for i, (_, k) in enumerate(data):
        app.tree.move(k, "", i)


def on_tree_select(app, g: dict, event):
    CENTER = g["CENTER"]
    HAS_CTK = g["HAS_CTK"]
    mol_to_photoimage = g["mol_to_photoimage"]

    sel = app.tree.selection()
    if not sel:
        return
    vals = app.tree.item(sel[0])["values"]
    if not vals:
        return
    cols = list(app.tree["columns"])
    smiles = vals[cols.index("SMILES_Final")]
    col_map = {
        "stats_score": "Compatibility_%",
        "stats_mw": "Molecular_Weight",
        "stats_logp": "LogP",
        "stats_tpsa": "TPSA",
        "stats_hba": "HBA",
        "stats_hbd": "HBD",
        "stats_qed": "QED",
        "stats_fsp3": "Fsp3",
        "stats_rb": "Rotatable_Bonds",
        "stats_rings": "Ring_Count",
        "stats_heavy": "Heavy_Atoms",
        "stats_mr": "Molar_Refractivity",
        "stats_pains": "PAINS_Alerts",
        "stats_brenk": "Brenk_Alerts",
        # Chirality / stereochemistry
        "stats_has_stereo": "Has_Stereo",
        "stats_chiral_centers": "Chiral_Centers",
    }
    for key, col_name in col_map.items():
        v = ""
        if col_name in cols:
            try:
                v = vals[cols.index(col_name)]
            except Exception:
                v = ""
        # Build a richer chirality summary line if we have the extra fields
        if key == "stats_chiral_centers":
            try:
                c_def = vals[cols.index("Chiral_Centers_Defined")] if "Chiral_Centers_Defined" in cols else ""
                c_un = vals[cols.index("Chiral_Centers_Unassigned")] if "Chiral_Centers_Unassigned" in cols else ""
                tags = vals[cols.index("Chiral_Tags")] if "Chiral_Tags" in cols else ""
                if str(v).strip() != "" and (str(c_def).strip() != "" or str(c_un).strip() != ""):
                    extra = f" (defined={c_def}, unassigned={c_un})"
                    if str(tags).strip():
                        extra += f" | {tags}"
                    v = f"{v}{extra}"
            except Exception:
                pass
        txt = f"{app.t(key)}: {v}"
        (app.stat_labels[key].configure(text=txt) if HAS_CTK else app.stat_labels[key].config(text=txt))
    app.canvas_2d.delete("all")
    img, err = mol_to_photoimage(str(smiles), (260, 200))
    if img:
        app._mol_img_ref = img
        try:
            cx = int(app.canvas_2d.winfo_width() / 2)
            cy = int(app.canvas_2d.winfo_height() / 2)
        except Exception:
            cx, cy = 140, 110
        app.canvas_2d.create_image(cx, cy, image=img)
    else:
        app._mol_img_ref = None
        msg = f"2D render unavailable\n\n{err}"
        try:
            cx = int(app.canvas_2d.winfo_width() / 2)
            cy = int(app.canvas_2d.winfo_height() / 2)
        except Exception:
            cx, cy = 140, 110
        app.canvas_2d.create_text(cx, cy, text=msg, fill="#888", font=app._get_font(13), justify=CENTER)
        if err == "RDKit/Pillow still loading":
            app.root.after(600, lambda: app._on_tree_select(None))

