from __future__ import annotations


def exp_bundle(app, g: dict):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]
    threading = g["threading"]
    pd = g.get("pd")
    _CHEM_READY = g["_CHEM_READY"]

    if not _CHEM_READY or pd is None:
        messagebox.showerror("Error", "RDKit + pandas required")
        return
    df = app.df_all
    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return
    fp = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP", "*.zip")])
    if not fp:
        return
    messagebox.showinfo(app.t("export_bundle_title"), app.t("export_bundle_msg"))

    def worker():
        try:
            out = app._export_research_bundle_zip(fp)
            app.root.after(0, lambda: messagebox.showinfo("OK", f"{app.t('saved')} {fp}\n\nFiles: {out.get('files', 0)}"))
        except Exception as ex:
            app.root.after(0, lambda: messagebox.showerror("Error", str(ex)))

    threading.Thread(target=worker, daemon=True).start()


def exp_paper(app, g: dict):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]
    threading = g["threading"]
    pd = g.get("pd")
    _CHEM_READY = g["_CHEM_READY"]

    if not _CHEM_READY or pd is None:
        messagebox.showerror("Error", "RDKit + pandas required")
        return
    df = app.df_all
    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return
    fp = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP", "*.zip")])
    if not fp:
        return
    messagebox.showinfo(app.t("export_paper_title"), app.t("export_paper_msg"))

    def worker():
        try:
            out = app._export_paper_dataset_zip(fp)
            app.root.after(0, lambda: messagebox.showinfo("OK", f"{app.t('saved')} {fp}\n\nFiles: {out.get('files', 0)}"))
        except Exception as ex:
            app.root.after(0, lambda: messagebox.showerror("Error", str(ex)))

    threading.Thread(target=worker, daemon=True).start()

