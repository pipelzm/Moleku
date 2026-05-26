from __future__ import annotations

from .smiles_utils import parse_smiles_flexible
from .ui_export_select import choose_export_dataframe


def exp_zip_3d(app, g: dict):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]
    zipfile = g["zipfile"]
    threading = g["threading"]
    Chem = g["Chem"]
    AllChem = g["AllChem"]
    _CHEM_READY = g["_CHEM_READY"]

    if not _CHEM_READY:
        messagebox.showerror("Error", "RDKit required")
        return
    df = app.df_all
    if df is None or getattr(df, "empty", True):
        messagebox.showinfo("!", app.t("no_datos"))
        return
    ideal_df = getattr(app, "df_ideal", None)
    manual_df = getattr(app, "df_admet_all", None)
    if manual_df is None or getattr(manual_df, "empty", True):
        manual_df = ideal_df if ideal_df is not None and not getattr(ideal_df, "empty", True) else df
    df_src = choose_export_dataframe(
        app,
        g,
        title_key="export_select_title_3d",
        ideal_df=ideal_df,
        manual_df=manual_df,
    )
    if df_src is None or getattr(df_src, "empty", True):
        return
    fp = filedialog.asksaveasfilename(defaultextension=".zip", filetypes=[("ZIP", "*.zip")])
    if not fp:
        return
    messagebox.showinfo(app.t("export_3d_title"), app.t("export_3d_msg"))

    def worker():
        try:
            written = 0
            skipped = 0

            with zipfile.ZipFile(fp, "w", zipfile.ZIP_DEFLATED) as zf:
                for idx, row in df_src.iterrows():
                    smi = row.get("SMILES_Final", "")
                    if not smi:
                        skipped += 1
                        continue
                    mol = parse_smiles_flexible(str(smi), Chem)
                    if not mol:
                        skipped += 1
                        continue
                    try:
                        mol = Chem.AddHs(mol)
                        # ETKDG gives better conformers
                        params = AllChem.ETKDGv3()
                        params.randomSeed = 42
                        ok = AllChem.EmbedMolecule(mol, params)
                        if ok != 0:
                            skipped += 1
                            continue
                        AllChem.MMFFOptimizeMolecule(mol, maxIters=200)
                        zf.writestr(f"mol_{idx}.sdf", Chem.MolToMolBlock(mol))
                        written += 1
                    except Exception:
                        skipped += 1
                        continue

            app.root.after(
                0,
                lambda: messagebox.showinfo(
                    "OK",
                    f"{app.t('saved')} {fp}\n\nWritten: {written}\nSkipped: {skipped}",
                ),
            )
        except Exception as ex:
            app.root.after(0, lambda: messagebox.showerror("Error", str(ex)))

    threading.Thread(target=worker, daemon=True).start()

