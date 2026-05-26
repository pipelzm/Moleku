from __future__ import annotations


def update_preview(app, g: dict):
    os = g["os"]
    HAS_CTK = g["HAS_CTK"]
    CL = g["CL"]
    CENTER = g["CENTER"]
    PREVIEW_CANVAS_HEIGHT = g["PREVIEW_CANVAS_HEIGHT"]
    MCR_CATALOGO = g["MCR_CATALOGO"]
    REACTION_PREVIEW_IMAGES = g["REACTION_PREVIEW_IMAGES"]
    resource_path = g["resource_path"]
    Image = g.get("Image")
    ImageTk = g.get("ImageTk")
    webbrowser = g["webbrowser"]

    if not hasattr(app, "preview_canvas") or not app.preview_canvas.winfo_exists():
        return
    cv = app.preview_canvas
    cv.delete("all")
    if hasattr(app, "_preview_img_refs"):
        app._preview_img_refs.clear()
    else:
        app._preview_img_refs = []

    mcr_key = app.mcr_var.get()
    preview = MCR_CATALOGO.get(mcr_key)
    if preview:
        lang = app.lang_var.get()
        desc = preview.get("info_es", "") if lang == "Español" else preview.get("info_en", preview.get("info_es", ""))
        doi = preview.get("doi", "N/A")
    else:
        desc, doi = "", "N/A"

    (app.lbl_preview_desc.configure(text=desc) if HAS_CTK else app.lbl_preview_desc.config(text=desc))
    (app.lbl_preview_doi.configure(text=f"DOI: {doi}") if HAS_CTK else app.lbl_preview_doi.config(text=f"DOI: {doi}"))

    if mcr_key in REACTION_PREVIEW_IMAGES and ImageTk is not None and Image is not None:
        img_path = resource_path(REACTION_PREVIEW_IMAGES[mcr_key])
        try:
            if os.path.exists(img_path):
                img = Image.open(img_path)
                cv.update_idletasks()
                canvas_width = cv.winfo_width() if cv.winfo_width() > 50 else 780
                canvas_height = cv.winfo_height() if cv.winfo_height() > 50 else PREVIEW_CANVAS_HEIGHT
                margin = 40
                max_w, max_h = canvas_width - margin, canvas_height - 80
                if img.size[0] > max_w or img.size[1] > max_h:
                    scale = min(max_w / img.size[0], max_h / img.size[1])
                    tw, th = int(img.size[0] * scale), int(img.size[1] * scale)
                    img = img.resize((tw, th), Image.Resampling.LANCZOS)
                else:
                    tw, th = img.size

                photo_img = ImageTk.PhotoImage(img)
                app._preview_img_refs.append(photo_img)
                x_center = canvas_width // 2
                y_center = (canvas_height // 2) + 10
                cv.create_image(x_center, y_center, image=photo_img, anchor=CENTER)
                cv.create_text(x_center, y_center + (th // 2) + 18, text=f"{mcr_key}", fill="#555555", font=app._get_font(11, True), anchor=CENTER)
                if doi and doi != "N/A":
                    app.lbl_preview_doi.bind("<Button-1>", lambda e: webbrowser.open(f"https://doi.org/{doi}"))
                return
        except Exception as e:
            print(f"Warning: Could not load preview image for {mcr_key}: {e}")

    cv.update_idletasks()
    cw = max(cv.winfo_width(), 520)
    cv.create_text(cw // 2, 80, text="⏳ Loading preview...", fill=CL["dim"], font=app._get_font(10))


def schedule_preview_redraw(app, g: dict):
    try:
        if getattr(app, "_preview_resize_job", None) is not None:
            app.root.after_cancel(app._preview_resize_job)
    except Exception:
        pass
    app._preview_resize_job = app.root.after(120, app._update_preview)

