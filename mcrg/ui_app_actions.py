from __future__ import annotations

from pathlib import Path
import zipfile


REACTION_EXAMPLE_PACKS = {
    "biginelli": {
        "label": "Biginelli (3-CR)",
        "files": ["aldehydes.csv", "beta_ketoesters.csv"],
        "notes": [
            "Seleccione Urea, Tiourea o Guanidina como reactivo central dentro de la app.",
            "Los archivos corresponden a Aldehídos y Beta-Cetoésteres.",
        ],
    },
    "gbb": {
        "label": "GBB (3-CR)",
        "files": ["aldehydes.csv", "isocyanides.csv", "aminoazines.csv"],
        "notes": [
            "Los archivos corresponden a Aldehídos, Isocianuros y 2-Aminoazinas.",
            "Incluye ejemplos con notación cargada para isocianuros.",
        ],
    },
    "gewald": {
        "label": "Gewald (3-CR)",
        "files": ["ketones.csv", "cyanoesters.csv"],
        "notes": [
            "Seleccione Azufre (S8) como reactivo central dentro de la app.",
            "Los archivos corresponden a Cetonas y Alfa-Cianoésteres.",
        ],
    },
}


def _examples_dir(g: dict) -> Path:
    resource_path = g.get("resource_path")
    if callable(resource_path):
        bundled = Path(resource_path("examples"))
        if bundled.exists():
            return bundled
    return Path(__file__).resolve().parent.parent / "examples"


def _build_pack_readme(pack_key: str) -> str:
    info = REACTION_EXAMPLE_PACKS[pack_key]
    lines = [
        f"Moleku example pack - {info['label']}",
        "",
        "Included files:",
    ]
    lines.extend(f"- {name}" for name in info["files"])
    lines.extend(
        [
            "",
            "Notes:",
        ]
    )
    lines.extend(f"- {note}" for note in info["notes"])
    lines.extend(
        [
            "",
            "These templates use NAME,SMILES and include compatible SMILES variants",
            "such as canonical, aromatic, alternate atom order, stereochemical, and",
            "charged representations when applicable.",
        ]
    )
    return "\n".join(lines) + "\n"


def _write_example_pack(examples_dir: Path, pack_key: str, output_path: str):
    info = REACTION_EXAMPLE_PACKS[pack_key]
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename in info["files"]:
            src = examples_dir / filename
            if not src.exists():
                raise FileNotFoundError(f"Missing example file: {src}")
            zf.write(src, arcname=filename)
        zf.writestr("README.txt", _build_pack_readme(pack_key))


def download_example_pack(app, g: dict, pack_key: str):
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]

    info = REACTION_EXAMPLE_PACKS.get(pack_key)
    if info is None:
        messagebox.showerror("Error", f"Unknown example pack: {pack_key}")
        return

    fp = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("ZIP", "*.zip"), ("All files", "*.*")],
        initialfile=f"moleku_{pack_key}_templates.zip",
        title=f"Save {info['label']} Example Pack",
    )
    if not fp:
        return

    try:
        examples_dir = _examples_dir(g)
        _write_example_pack(examples_dir, pack_key, fp)
        messagebox.showinfo(
            "✅ Success",
            f"Example pack saved successfully:\n{fp}\n\nIncludes: {', '.join(info['files'])}",
        )
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to save example pack:\n{e}")


def restart_app(app, g: dict):
    messagebox = g["messagebox"]
    if messagebox.askyesno(app.t("reiniciar"), app.t("restart_confirm")):
        app._clear_results()
        app._refresh_slots()
        app._update_labels()
        app._switch_tab("motor")


def download_example(app, g: dict, fmt: str):
    pd = g.get("pd")
    messagebox = g["messagebox"]
    filedialog = g["filedialog"]

    if pd is None:
        messagebox.showerror("Error", "Pandas is required to generate templates.")
        return
    fp = filedialog.asksaveasfilename(
        defaultextension=f".{fmt}",
        filetypes=[(fmt.upper(), f"*.{fmt}"), ("All files", "*.*")],
        title=f"Save {fmt.upper()} Example Template",
    )
    if not fp:
        return
    try:
        data = {
            "NAME": [
                "Benzaldehyde",
                "4-Methoxybenzaldehyde",
                "4-Nitrobenzaldehyde",
                "Furfural",
                "Cinnamaldehyde_E",
                "2-Naphthaldehyde",
                "Salicylaldehyde",
            ],
            "SMILES": [
                "c1ccccc1C=O",
                "COc1ccc(C=O)cc1",
                "O=Cc1ccc([N+](=O)[O-])cc1",
                "O=Cc1ccco1",
                "O=C/C=C/c1ccccc1",
                "C1=CC=C2C=CC=CC2=C1C=O",
                "Oc1ccccc1C=O",
            ],
        }
        df = pd.DataFrame(data)
        if fmt == "csv":
            df.to_csv(fp, index=False, sep=",", encoding="utf-8")
        elif fmt == "txt":
            df.to_csv(fp, index=False, sep="\t", encoding="utf-8")
        elif fmt == "xlsx":
            df.to_excel(fp, index=False, engine="openpyxl")
        messagebox.showinfo("✅ Success", f"Template saved successfully:\n{fp}")
    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to save template:\n{e}")


def open_feedback(app, g: dict):
    """
    Open the feedback/reporting page for this release.
    Kept intentionally simple so it works in PyInstaller builds across OSes.
    """
    webbrowser = g.get("webbrowser")
    messagebox = g.get("messagebox")
    url = getattr(app, "feedback_url", "") or ""
    if not url:
        try:
            messagebox.showinfo("Feedback", "Feedback URL is not configured.")
        except Exception:
            pass
        return
    try:
        if webbrowser is not None:
            webbrowser.open(url)
    except Exception:
        try:
            messagebox.showinfo("Feedback", url)
        except Exception:
            pass

