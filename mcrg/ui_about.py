from __future__ import annotations


def build_about(app, g: dict):
    tk = g["tk"]
    ctk = g.get("ctk")
    HAS_CTK = g["HAS_CTK"]
    CL = g["CL"]
    X = g["X"]
    Y = g["Y"]
    BOTH = g["BOTH"]
    LEFT = g["LEFT"]
    RIGHT = g["RIGHT"]
    VERTICAL = g["VERTICAL"]
    webbrowser = g["webbrowser"]
    messagebox = g["messagebox"]
    resource_path = g["resource_path"]
    os = g["os"]
    Image = g.get("Image")

    fr = app.tab_frames["acerca"]
    if HAS_CTK:
        scroll = ctk.CTkScrollableFrame(fr, fg_color=CL["bg"])
        scroll.pack(fill=BOTH, expand=True, padx=16, pady=12)
    else:
        canvas = tk.Canvas(fr, bg=CL["bg"], highlightthickness=0)
        sb = tk.Scrollbar(fr, orient=VERTICAL, command=canvas.yview)
        scroll = tk.Frame(canvas, bg=CL["bg"])
        scroll.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        sb.pack(side=RIGHT, fill=Y)

    inner = scroll
    try:
        inner.columnconfigure(0, weight=1)
    except Exception:
        pass

    app._about_logo_ref = None
    try:
        logo_path = resource_path("images/moleku_logo.png")
        if not os.path.exists(logo_path):
            for _fallback in ("images/mcrg_logo_simple.png", "images/mcrg_logo.png"):
                _alt = resource_path(_fallback)
                if os.path.exists(_alt):
                    logo_path = _alt
                    break
        if os.path.exists(logo_path):
            if HAS_CTK and Image is not None:
                pil = Image.open(logo_path).convert("RGBA")
                pil.thumbnail((120, 120))
                cimg = ctk.CTkImage(light_image=pil, dark_image=pil, size=pil.size)
                app.lbl_about_logo = ctk.CTkLabel(inner, text="", image=cimg)
                app._about_logo_ref = cimg
                app.lbl_about_logo.grid(row=0, column=0, pady=(10, 8))
            else:
                img = tk.PhotoImage(file=logo_path)
                w, h = img.width(), img.height()
                if max(w, h) > 140:
                    f = max(1, int(max(w, h) / 120))
                    img = img.subsample(f, f)
                app.lbl_about_logo = tk.Label(inner, image=img, bg=CL["bg"])
                app._about_logo_ref = img
                app.lbl_about_logo.grid(row=0, column=0, pady=(10, 8))
    except Exception:
        pass

    app.fr_about_desc = app._frame(inner, fg_color=CL["bg2"] if HAS_CTK else None, corner_radius=6)
    app.fr_about_desc.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
    app.lbl_about_desc = app._lbl(app.fr_about_desc, text="", font=app._get_font(16), text_color=CL["dim"], justify="center", wraplength=720)
    if not HAS_CTK:
        app.lbl_about_desc.config(bg=CL["bg2"])
    app.lbl_about_desc.pack(padx=15, pady=12)

    fr_credits = app._frame(inner, fg_color=CL["bg"] if HAS_CTK else None)
    fr_credits.grid(row=2, column=0, pady=8)
    app._lbl(fr_credits, text="Developed by: ", font=app._get_font(13, True), text_color=CL["fg"]).pack(side=LEFT)
    app._make_hyperlink(fr_credits, "Felipe Lizama Mora", "https://github.com/pipelzm", 13)
    app._lbl(fr_credits, text=" @ ", font=app._get_font(13, True), text_color=CL["fg"]).pack(side=LEFT)
    app._make_hyperlink(fr_credits, "SB&BCS Lab", "https://sites.google.com/view/sbbcs-ufro/news?authuser=0", 13)
    app._lbl(fr_credits, text=" | ", font=app._get_font(13, True), text_color=CL["fg"]).pack(side=LEFT)
    app._make_hyperlink(fr_credits, "UFRO", "https://www.ufro.cl", 13)

    fr_btns = app._frame(inner, fg_color=CL["bg"] if HAS_CTK else None)
    fr_btns.grid(row=3, column=0, pady=12)
    app._btn(fr_btns, text="LinkedIn", width=140, height=30, fg_color=CL["accent"], hover_color=CL["accent2"], text_color="#fff", font=app._get_font(10), command=lambda: webbrowser.open("https://www.linkedin.com/in/felipe-lizama-mora-6b8685256/")).pack(side=LEFT, padx=(0, 10))
    app._btn(fr_btns, text="Personal Web", width=140, height=30, fg_color=CL["bg3"], hover_color=CL["border"], text_color=CL["fg"], font=app._get_font(10), command=lambda: messagebox.showinfo("Coming Soon", "Personal website will be available soon.")).pack(side=LEFT, padx=(0, 10))

    app.lbl_about_footer = app._lbl(inner, text=app.t("about_footer"), font=app._get_font(13, True), text_color=CL["dim"], justify="center")
    if not HAS_CTK:
        app.lbl_about_footer.config(bg=CL["bg"])
    app.lbl_about_footer.grid(row=4, column=0, pady=(10, 5))

