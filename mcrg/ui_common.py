from __future__ import annotations


def col_label(app, g: dict, col: str) -> str:
    """
    Translate table column headers based on current UI language.
    Keeps internal dataframe column keys stable.
    """
    lang = app.lang_var.get()
    es = lang == "Español"

    # Core descriptor / status columns
    core_map = {
        "Compatibility_%": ("Compatibility %", "Compatibilidad %"),
        "Classification": ("Classification", "Clasificación"),
        "Failure_Reason": ("Failure reason", "Motivo de descarte"),
        "SMILES_Final": ("Final SMILES", "SMILES final"),
        "InChIKey": ("InChIKey", "InChIKey"),
        "Is_Duplicate": ("Duplicate?", "¿Duplicado?"),
        "Duplicate_Of": ("Duplicate of", "Duplicado de"),
        "Candidate_Name": ("Candidate", "Candidato"),
        "Core_Reagent": ("Core reagent", "Reactivo central"),
        "Ideal_Rule": ("Ideal rule", "Regla ideal"),
        "Molecular_Weight": ("Molecular weight (Da)", "Peso molecular (Da)"),
        "LogP": ("LogP", "LogP"),
        "TPSA": ("tPSA (Å²)", "tPSA (Å²)"),
        "HBA": ("H-bond acceptors", "Aceptores de H"),
        "HBD": ("H-bond donors", "Donadores de H"),
        "Rotatable_Bonds": ("Rotatable bonds", "Enlaces rotables"),
        "Heavy_Atoms": ("Heavy atoms", "Átomos pesados"),
        "Ring_Count": ("Ring count", "Número de anillos"),
        "Molar_Refractivity": ("Molar refractivity", "Refractividad molar"),
        "QED": ("QED", "QED"),
        "Fsp3": ("Fsp3", "Fsp3"),
        "PAINS_Alerts": ("PAINS alerts", "Alertas PAINS"),
        "Brenk_Alerts": ("Brenk alerts", "Alertas Brenk"),
        "Pass_Lipinski": ("Pass Lipinski", "Pasa Lipinski"),
        "Pass_Ghose": ("Pass Ghose", "Pasa Ghose"),
        "Pass_Veber": ("Pass Veber", "Pasa Veber"),
        "Pass_Egan": ("Pass Egan", "Pasa Egan"),
        "Pass_Muegge": ("Pass Muegge", "Pasa Muegge"),
        # Chirality / stereochemistry
        "Has_Stereo": ("Has stereochemistry?", "¿Tiene estereo?"),
        "Chiral_Centers": ("Chiral centers", "Centros quirales"),
        "Chiral_Centers_Defined": ("Chiral centers (defined)", "Centros quirales (definidos)"),
        "Chiral_Centers_Unassigned": ("Chiral centers (unassigned)", "Centros quirales (sin asignar)"),
        "Chiral_Tags": ("Chiral tags", "Etiquetas quirales"),
    }
    if col in core_map:
        return core_map[col][1] if es else core_map[col][0]

    # Reaction component columns come from the catalog (Spanish names).
    component_map_en = {
        "Aldehídos": "Aldehydes",
        "Beta-Cetoésteres": "β-Ketoesters",
        "Aldehídos/Cetonas": "Aldehydes/Ketones",
        "Ácidos Carboxílicos": "Carboxylic acids",
        "Isocianuros": "Isocyanides",
        "Aminas Sec/Prim": "Secondary/Primary amines",
        "Carbonilos Enolizables": "Enolizable carbonyls",
        "Aminas": "Amines",
        "Ácidos Borónicos": "Boronics acids",
        "Fosfitos Dialquílicos": "Dialkyl phosphites",
        "2-Aminoazinas": "2-Aminoazines",
        "Anilinas": "Anilines",
        "Cetonas": "Ketones",
        "Alfa-Cianoésteres": "α-Cyanoesters",
        "Beta-Cetoéster (Equiv 1)": "β-Ketoester (Equiv 1)",
        "Beta-Cetoéster (Equiv 2)": "β-Ketoester (Equiv 2)",
        "Aminas Primarias": "Primary amines",
        "Fenoles": "Phenols",
        "Alfa-Halo Carbonilos": "α-Halo carbonyls",
        "Amoniaco/Aminas": "Ammonia/Amines",
        "Carbonilos": "Carbonyls",
    }
    if col in component_map_en:
        return col if es else component_map_en[col]

    if col.endswith("_SMILES"):
        base = col[:-7]
        base_label = base
        if base in component_map_en:
            base_label = base if es else component_map_en[base]
        if es:
            return f"SMILES ({base_label})"
        return f"{base_label} SMILES"

    return col


def get_font(app, g: dict, base_size, bold: bool = False):
    return ("Helvetica Neue", int(base_size), "bold" if bold else "normal")


def btn(app, g: dict, p, **kw):
    HAS_CTK = g["HAS_CTK"]
    ctk = g["ctk"]
    tk = g["tk"]
    CL = g["CL"]

    if HAS_CTK:
        return ctk.CTkButton(p, **kw)
    tk_kw = {k: v for k, v in kw.items() if k not in ("text_color", "fg_color", "hover_color", "corner_radius")}
    tk_kw["bg"] = kw.get("fg_color", CL["bg3"])
    tk_kw["fg"] = kw.get("text_color", CL["fg"])
    if "font" not in tk_kw:
        tk_kw["font"] = app._get_font(12)
    return tk.Button(p, bd=1, relief="flat", **tk_kw)


def lbl(app, g: dict, p, **kw):
    HAS_CTK = g["HAS_CTK"]
    ctk = g["ctk"]
    tk = g["tk"]
    CL = g["CL"]

    if HAS_CTK:
        return ctk.CTkLabel(p, **kw)
    tk_kw = {k: v for k, v in kw.items() if k not in ("text_color", "fg_color")}
    tk_kw["bg"] = kw.get("fg_color", CL["bg"])
    tk_kw["fg"] = kw.get("text_color", CL["fg"])
    if "font" not in tk_kw:
        tk_kw["font"] = app._get_font(12)
    return tk.Label(p, **tk_kw)


def frame(app, g: dict, p, **kw):
    HAS_CTK = g["HAS_CTK"]
    ctk = g["ctk"]
    tk = g["tk"]
    CL = g["CL"]

    if HAS_CTK:
        return ctk.CTkFrame(p, **kw)
    tk_kw = {k: v for k, v in kw.items() if k not in ("fg_color", "corner_radius", "border_width", "border_color")}
    tk_kw["bg"] = kw.get("fg_color", CL["bg"])
    return tk.Frame(p, **tk_kw)


def build_ui(app, g: dict):
    HAS_CTK = g["HAS_CTK"]
    ctk = g["ctk"]
    tk = g["tk"]
    ttk = g["ttk"]
    CL = g["CL"]
    LOCALES = g["LOCALES"]
    X = g["X"]
    BOTH = g["BOTH"]
    LEFT = g["LEFT"]
    RIGHT = g["RIGHT"]

    tb = ctk.CTkFrame(app.root, height=40, fg_color=CL["bg2"]) if HAS_CTK else tk.Frame(app.root, bg=CL["bg2"], height=40)
    tb.pack(fill=X)
    tb.pack_propagate(False)
    app.lbl_title = app._lbl(tb, text=app.t("titulo"), font=app._get_font(16, True), text_color=CL["accent"])
    app.lbl_title.pack(side=LEFT, padx=14)
    fr_r = app._frame(tb, fg_color=CL["bg2"])
    fr_r.pack(side=RIGHT, padx=10)

    # Feedback button (v1.0 core)
    try:
        app.btn_feedback = app._btn(
            fr_r,
            text=app.t("feedback"),
            width=110,
            height=28,
            fg_color=CL["bg3"],
            hover_color=CL["border"],
            text_color=CL["fg"],
            font=app._get_font(11, True),
            command=app._open_feedback,
        )
        app.btn_feedback.pack(side=RIGHT, padx=(0, 8))
    except Exception:
        app.btn_feedback = None

    if HAS_CTK:
        ctk.CTkComboBox(fr_r, variable=app.lang_var, values=list(LOCALES.keys()), width=110, command=lambda v: app._on_lang_change()).pack(side=RIGHT)
    else:
        cb = ttk.Combobox(fr_r, textvariable=app.lang_var, values=list(LOCALES.keys()), state="readonly", width=10)
        cb.pack(side=RIGHT)
        cb.bind("<<ComboboxSelected>>", lambda e: app._on_lang_change())

    tk.Frame(app.root, bg=CL["accent"], height=3).pack(fill=X)
    tb2 = ctk.CTkFrame(app.root, height=36, fg_color=CL["bg2"]) if HAS_CTK else tk.Frame(app.root, bg=CL["bg2"], height=36)
    tb2.pack(fill=X)
    tb2.pack_propagate(False)
    app.current_tab = "motor"
    app.tab_btns = {}
    for tid in app.TAB_IDS:
        cls = (
            ctk.CTkButton(tb2, text="", width=140, height=30, font=app._get_font(13, True), command=lambda t=tid: app._switch_tab(t))
            if HAS_CTK
            else tk.Button(tb2, text="", bd=0, font=app._get_font(13, True), cursor="hand2", command=lambda t=tid: app._switch_tab(t))
        )
        cls.pack(side=LEFT, padx=2, pady=3)
        app.tab_btns[tid] = cls

    app.container = app._frame(app.root, fg_color=CL["bg"])
    app.container.pack(fill=BOTH, expand=True)
    app.container.rowconfigure(0, weight=1)
    app.container.columnconfigure(0, weight=1)
    app.tab_frames = {}
    for tid in app.TAB_IDS:
        f = app._frame(app.container, fg_color=CL["bg"])
        app.tab_frames[tid] = f
        f.grid(row=0, column=0, sticky="nsew")
        f.grid_remove()

    app._build_motor()
    app._build_resultados()
    if "admet" in getattr(app, "TAB_IDS", []):
        app._build_admet()
    if "espacio" in getattr(app, "TAB_IDS", []):
        app._build_espacio()
    app._build_guide()
    app._build_acerca()
    app._update_labels()
    app._switch_tab("motor")
    app.root.after(1500, app._update_preview)

