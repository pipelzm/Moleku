from __future__ import annotations


def run_clicked(app, g: dict):
    # This is the extracted body of MCRGApp._run
    _CHEM_READY = g["_CHEM_READY"]
    pd = g["pd"]
    Image = g["Image"]
    HAS_CTK = g["HAS_CTK"]
    DISABLED = g["DISABLED"]
    NORMAL = g["NORMAL"]
    messagebox = g["messagebox"]
    os = g["os"]
    threading = g["threading"]
    time = g["time"]
    MCR_CATALOGO = g["MCR_CATALOGO"]
    BooleanVar = g["BooleanVar"]
    run_mcr = g["run_mcr"]

    if not _CHEM_READY or pd is None or Image is None:
        missing = []
        if not _CHEM_READY:
            missing.append("RDKit")
        if pd is None:
            missing.append("pandas")
        if Image is None:
            missing.append("Pillow (PIL)")
        messagebox.showerror(
            app.t("missing_libraries") if hasattr(app, "t") else "Missing Libraries",
            f"Not ready / missing: {', '.join(missing)}\n\nTip: wait a few seconds after opening the app, or install missing packages.",
        )
        return

    mcr = app.mcr_var.get()
    paths = []
    for c in MCR_CATALOGO[mcr]["componentes"]:
        fp = app.file_paths.get(c)
        if not fp or not os.path.isfile(fp):
            messagebox.showwarning("!", app.t("error_archivos"))
            return
        paths.append(fp)

    core_smiles_list = []
    opts = MCR_CATALOGO[mcr].get("opciones_centrales", {})
    if opts:
        for name, smi in opts.items():
            if app.central_vars.get(name, BooleanVar(value=False)).get():
                core_smiles_list.append((name, smi))
        if not core_smiles_list:
            first_name = next(iter(opts.keys()))
            core_smiles_list = [(first_name, opts[first_name])]

    (app.btn_start.configure(state="disabled") if HAS_CTK else app.btn_start.config(state=DISABLED))
    (app.lbl_status.configure(text=app.t("procesando")) if HAS_CTK else app.lbl_status.config(text=app.t("procesando")))
    try:
        if HAS_CTK:
            app.pbar.set(0.0)
        else:
            app.pbar["value"] = 0
    except Exception:
        pass

    thr = app.threshold_var.get()
    try:
        app._last_run_context = {
            "mcr": mcr,
            "threshold": float(thr),
            "component_files": {c: app.file_paths.get(c, "") for c in MCR_CATALOGO[mcr]["componentes"]},
            "core_reagents": list(core_smiles_list),
        }
    except Exception:
        app._last_run_context = {}

    def worker():
        try:
            last_ui_t = [0.0]
            last_ui_cur = [-1]

            def cb(cur, tot):
                now = time.monotonic()
                pct = (cur / tot) if tot > 0 else 0.0
                pct = max(0.0, min(1.0, pct))
                should_update = (cur == tot) or (cur == 0) or (now - last_ui_t[0] >= 0.05) or (cur - last_ui_cur[0] >= 250)
                if not should_update:
                    return
                last_ui_t[0] = now
                last_ui_cur[0] = cur

                def _ui():
                    if HAS_CTK:
                        try:
                            app.pbar.set(pct)
                        except Exception:
                            pass
                        try:
                            app.lbl_status.configure(text=f"{cur}/{tot} ({pct*100:.0f}%)")
                        except Exception:
                            app.lbl_status.config(text=f"{cur}/{tot} ({pct*100:.0f}%)")
                    else:
                        try:
                            app.pbar["value"] = pct * 100.0
                        except Exception:
                            try:
                                app.pbar.configure(value=pct * 100.0)
                            except Exception:
                                pass
                        app.lbl_status.config(text=f"{cur}/{tot} ({pct*100:.0f}%)")

                app.root.after(0, _ui)

            df_all, df_ideal, preview = run_mcr(
                mcr,
                paths,
                core_smiles_list,
                thr,
                cb,
                standardize=bool(app.standardize_var.get()),
                ideal_rule=str(app.ideal_rule_var.get()),
            )
            app.df_all, app.df_ideal = df_all, df_ideal

            def finish():
                na = len(df_all) if df_all is not None else 0
                ni = len(df_ideal) if df_ideal is not None else 0
                app.total_generated = na
                app.total_discarded = na - ni
                (app.lbl_status.configure(text=f"{app.t('listo')} {na} {app.t('productos')}") if HAS_CTK else app.lbl_status.config(text=f"{app.t('listo')} {na} {app.t('productos')}"))
                (app.lbl_combinations.configure(text=f"📊 Total: {app.total_generated} | ✅ Ideal: {app.total_generated - app.total_discarded} | ❌ Discarded: {app.total_discarded}") if HAS_CTK else app.lbl_combinations.config(text=f"📊 Total: {app.total_generated} | ✅ Ideal: {app.total_generated - app.total_discarded} | ❌ Discarded: {app.total_discarded}"))
                app.console.config(state=g["NORMAL"])
                app.console.delete("1.0", g["END"])
                app.console.insert(g["END"], preview)
                app.console.config(state=g["DISABLED"])
                if na == 0:
                    error_msg = "\n🔍 DEBUG INFO:\n" + preview + "\n\n✅ TRY THIS:\n1️⃣ Check file format (NAME and SMILES columns)\n2️⃣ Ensure SMILES are valid\n3️⃣ Threshold is now 0 - should accept ALL products\n4️⃣ Check reactants have groups needed for reaction\n\nℹ️ See console above for detailed diagnostics"
                    messagebox.showwarning("⚠️ No Products Generated", error_msg)
                    return
                app.filter_var.set("Ideal")
                app._apply_filter()
                app._draw_plots()
                app._switch_tab("resultados")

            app.root.after(0, finish)
        except Exception as ex:
            app.root.after(0, lambda: messagebox.showerror("Error", str(ex)))
        finally:
            app.root.after(0, lambda: (app.btn_start.configure(state="normal") if HAS_CTK else app.btn_start.config(state=NORMAL)))

    threading.Thread(target=worker, daemon=True).start()

