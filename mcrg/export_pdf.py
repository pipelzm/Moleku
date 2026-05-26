from __future__ import annotations


def export_pdf(app, g: dict, df, fp: str):
    messagebox = g["messagebox"]
    try:
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.pagesizes import letter, landscape
    except Exception:
        messagebox.showerror(
            "Missing Library",
            "PDF export requires the 'reportlab' package.\n\nInstall:\n  pip install reportlab",
        )
        return

    cols = [
        "Compatibility_%",
        "Molecular_Weight",
        "LogP",
        "TPSA",
        "HBA",
        "HBD",
        "Rotatable_Bonds",
        "Ring_Count",
        "Pass_Lipinski",
        "Pass_Ghose",
        "Pass_Veber",
        "Pass_Egan",
        "Pass_Muegge",
        "Ideal_Rule",
        "Core_Reagent",
        "Classification",
        "SMILES_Final",
    ]
    cols = [c for c in cols if c in df.columns]

    def safe_str(v):
        if v is None:
            return ""
        s = str(v)
        return s.replace("\n", " ").strip()

    try:
        c = rl_canvas.Canvas(fp, pagesize=landscape(letter))
        w, h = landscape(letter)
        left = 40
        top = h - 40
        y = top

        title = f"Moleku Results ({len(df)} rows)"
        c.setFont("Helvetica-Bold", 14)
        c.drawString(left, y, title)
        y -= 22

        c.setFont("Helvetica", 8)
        header = " | ".join(cols)
        c.drawString(left, y, header[:180])
        y -= 14
        c.setLineWidth(0.5)
        c.line(left, y, w - left, y)
        y -= 10

        line_height = 10
        max_chars = 220
        for _, row in df.iterrows():
            parts = [safe_str(row.get(col, "")) for col in cols]
            line = " | ".join(parts)
            if len(line) > max_chars:
                line = line[: max_chars - 3] + "..."
            c.drawString(left, y, line)
            y -= line_height
            if y < 40:
                c.showPage()
                y = top
                c.setFont("Helvetica-Bold", 10)
                c.drawString(left, y, title)
                y -= 18
                c.setFont("Helvetica", 8)
                c.drawString(left, y, header[:180])
                y -= 14
                c.line(left, y, w - left, y)
                y -= 10

        c.save()
        messagebox.showinfo("OK", f"{app.t('saved')} {fp}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export PDF:\n{e}")

