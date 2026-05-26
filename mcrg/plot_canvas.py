from __future__ import annotations


def render_espacio(app, g: dict):
    tk = g["tk"]
    HAS_CTK = g["HAS_CTK"]
    PLOT_DESC = g["PLOT_DESC"]

    if getattr(app, "_updating_plots", False):
        return
    try:
        app._updating_plots = True
        current_config = (app.plot_var.get(), app.versus_var.get(), app.lang_var.get())
        if getattr(app, "_last_plot_config", None) == current_config:
            return
        app._last_plot_config = current_config

        for w in app.plot_inner_frame.winfo_children():
            w.destroy()
        app._plot_canvases = []

        versus_mode = app.versus_var.get()
        primary_plot = app.plot_var.get()

        def _plot_key_from_display(val: str) -> str:
            if val in app._plot_keys:
                return val
            for k in app._plot_keys:
                if app.t(k) == val:
                    return k
            return val

        def _set_plot_description(primary_val: str, versus_val: str):
            lang = app.lang_var.get()
            lang_key = "es" if lang == "Español" else "en"
            p_key = _plot_key_from_display(primary_val)
            v_key = _plot_key_from_display(versus_val) if versus_val and versus_val != "Off" else None

            def _desc_for(k: str) -> str:
                d = PLOT_DESC.get(k, {})
                return d.get(lang_key, d.get("en", "")) if isinstance(d, dict) else ""

            if v_key and v_key != p_key:
                if lang_key == "es":
                    header = f"Modo Versus: comparando '{p_key}' vs '{v_key}'."
                    meaning = "Esta comparativa te permite ver diferencias de distribución entre dos métricas para el mismo conjunto de resultados."
                else:
                    header = f"Versus Mode: comparing '{p_key}' vs '{v_key}'."
                    meaning = "This comparison helps you visually contrast the distributions of two metrics over the same results set."
                body = "\n\n".join([_desc_for(p_key), _desc_for(v_key)])
                text = header + "\n" + meaning + ("\n\n" + body if body.strip() else "")
            else:
                text = _desc_for(p_key)

            if getattr(app, "lbl_plot_desc", None):
                (app.lbl_plot_desc.configure(text=text) if HAS_CTK else app.lbl_plot_desc.config(text=text))

        if versus_mode != "Off" and versus_mode != primary_plot:
            plots_to_draw = [primary_plot, versus_mode]
            cols = 2
        else:
            plots_to_draw = [primary_plot]
            cols = 1

        _set_plot_description(primary_plot, versus_mode)

        for c in range(cols):
            app.plot_inner_frame.columnconfigure(c, weight=1)
        r, c_idx = 0, 0
        for key in plots_to_draw:
            cw = 600 if cols == 2 else 820
            ch = 440 if cols == 2 else 560
            cv = tk.Canvas(app.plot_inner_frame, width=cw, height=ch, bg="#ffffff", highlightthickness=2, highlightbackground="#000000")
            cv.grid(row=r, column=c_idx, sticky="nsew", padx=8, pady=8)
            app._plot_canvases.append((cv, key))
            c_idx += 1
            if c_idx >= cols:
                c_idx = 0
                r += 1
            app.plot_inner_frame.rowconfigure(r, weight=1)

        draw_plots(app, g)
    finally:
        app._updating_plots = False


def draw_plots(app, g: dict):
    if not getattr(app, "_plot_canvases", None):
        return
    df_all = getattr(app, "df_all", None)
    if df_all is None or getattr(df_all, "empty", True):
        for cv, key in app._plot_canvases:
            draw_empty_state(app, g, cv, key)
        return

    cache_key = (tuple(k for _, k in app._plot_canvases), app.filter_var.get(), app.lang_var.get())
    if not hasattr(app, "_plot_cache") or app._plot_cache is None:
        app._plot_cache = {}
    for cv, key in app._plot_canvases:
        try:
            if cache_key in app._plot_cache and key in app._plot_cache[cache_key]:
                render_from_cache(app, g, cv, key, app._plot_cache[cache_key][key])
            else:
                data = prepare_plot_data(app, g, key)
                draw_single_plot(app, g, cv, key, data)
                if cache_key not in app._plot_cache:
                    app._plot_cache[cache_key] = {}
                app._plot_cache[cache_key][key] = data
        except Exception as e:
            print(f"Error rendering plot {key}: {e}")


def prepare_plot_data(app, g: dict, plot_key: str) -> dict:
    pd = g["pd"]
    df = app.df_all
    try:
        if df is not None and not getattr(df, "empty", True) and "Classification" in df.columns:
            fv = app.filter_var.get()
            if fv == "Ideal":
                df = df[df["Classification"] == "Ideal"]
            elif fv == "Discard":
                df = df[df["Classification"] != "Ideal"]
    except Exception:
        df = app.df_all
    if df is None or getattr(df, "empty", True):
        return {}

    def _num_series(frame, col):
        try:
            s = pd.to_numeric(frame[col], errors="coerce")
            s = s.dropna()
            return s
        except Exception:
            return pd.Series([], dtype="float64")

    if plot_key.endswith("by Classification"):
        col = "Molecular_Weight" if plot_key.startswith("MW") else "LogP"
        ideal_s = _num_series(df[df["Classification"] == "Ideal"], col)
        disc_s = _num_series(df[df["Classification"] != "Ideal"], col)
        feature_key = "MW" if plot_key.startswith("MW") else "LogP"
        return {"ideal": ideal_s.tolist(), "discard": disc_s.tolist(), "feature_key": feature_key}
    if plot_key.endswith("Distribution"):
        col_map = {
            "Score Distribution": "Compatibility_%",
            "MW Distribution": "Molecular_Weight",
            "LogP Distribution": "LogP",
            "TPSA Distribution": "TPSA",
            "HBA Distribution": "HBA",
            "HBD Distribution": "HBD",
        }
        col_name = col_map.get(plot_key)
        if not col_name or col_name not in df.columns:
            return {}
        vals_s = _num_series(df, col_name)
        return {"values": vals_s.tolist(), "col_name": plot_key.replace(" Distribution", "")}
    if plot_key.startswith("2D PCA"):
        cols = ["Molecular_Weight", "LogP", "TPSA", "HBA", "HBD"]
        if not all(c in df.columns for c in cols):
            return {}
        try:
            import numpy as _np

            X = []
            is_ideal = []
            for _, row in df.iterrows():
                vals = []
                ok = True
                for c in cols:
                    try:
                        v = float(row.get(c, ""))
                    except Exception:
                        ok = False
                        break
                    if not _np.isfinite(v):
                        ok = False
                        break
                    vals.append(v)
                if not ok:
                    continue
                X.append(vals)
                is_ideal.append(str(row.get("Classification", "")) == "Ideal")
            if not X:
                return {}
            X = _np.asarray(X, dtype=float)
            mu = X.mean(axis=0)
            sd = X.std(axis=0)
            sd[sd == 0] = 1.0
            Z = (X - mu) / sd
            _U, _S, Vt = _np.linalg.svd(Z, full_matrices=False)
            comps = Z @ Vt.T
            pts = [(float(comps[i, 0]), float(comps[i, 1]), bool(is_ideal[i])) for i in range(comps.shape[0])]
            return {"points": pts, "method": "PCA_SVD", "columns": cols}
        except Exception:
            return {}
    return {}


def draw_empty_state(app, g: dict, cv, key: str):
    cw, ch = cv.winfo_width(), cv.winfo_height()
    cv.delete("all")
    cv.create_text(cw // 2, ch // 2, text=app.t("sin_datos"), fill="#888", font=app._get_font(11))


def render_from_cache(app, g: dict, cv, key: str, data: dict):
    cv.delete("all")
    draw_single_plot(app, g, cv, key, data)


def get_xlabel(app, key: str) -> str:
    if key.startswith("MW"):
        return "Molecular weight (Da)"
    if key.startswith("TPSA"):
        return "TPSA (Å²)"
    if key.startswith("LogP"):
        return "LogP"
    if key.startswith("HBA"):
        return "HBA"
    if key.startswith("HBD"):
        return "HBD"
    if key.startswith("Score"):
        return "Heuristic compatibility (%)"
    if key.startswith("2D PCA"):
        return "PC1"
    return "Value"


def get_ylabel(app, key: str) -> str:
    if "Distribution" in key:
        return "Frequency"
    if "by Classification" in key:
        return "Count"
    if key.startswith("2D PCA"):
        return "PC2"
    return "Count"


def draw_single_plot(app, g: dict, cv, key: str, data: dict):
    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    cw, ch = cv.winfo_width(), cv.winfo_height()
    if cw < 50:
        cw = 600 if app.versus_var.get() != "Off" else 820
    if ch < 50:
        ch = 440 if app.versus_var.get() != "Off" else 560
    m = 92 if app.versus_var.get() != "Off" else 104
    cv.delete("all")

    create_professional_plot_template(app, g, cv, cw, ch, m, key, get_xlabel(app, key), get_ylabel(app, key))

    if key.endswith("Distribution"):
        draw_histogram(app, g, cv, cw, ch, m, data)
    elif key.endswith("by Classification"):
        draw_class_hist(app, g, cv, cw, ch, m, data)
    elif key.startswith("2D PCA"):
        draw_embedding_2d(app, g, cv, cw, ch, m, data)


def draw_embedding_2d(app, g: dict, cv, cw: int, ch: int, m: int, data: dict):
    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    pts = data.get("points", [])
    if not pts:
        draw_empty_state(app, g, cv, "")
        return
    s = PLOT_SETTINGS
    axc = s.get("axis_color", "#000000")
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    span_x = (max_x - min_x) if (max_x - min_x) != 0 else 1.0
    span_y = (max_y - min_y) if (max_y - min_y) != 0 else 1.0
    w = cw - 2 * m
    h = ch - 2 * m
    r = 2
    for x, y, is_ideal in pts:
        px = m + ((x - min_x) / span_x) * w
        py = ch - m - ((y - min_y) / span_y) * h
        col = s.get("color_ideal", "#27ae60") if is_ideal else s.get("color_discard", "#c0392b")
        cv.create_oval(px - r, py - r, px + r, py + r, fill=col, outline=axc, width=0)
    leg_title = "Leyenda" if app.lang_var.get() == "Español" else "Legend"
    draw_plot_legend(app, g, cv, cw, ch, m, leg_title, [(app.t("ideal"), s["color_ideal"]), (app.t("descartado"), s["color_discard"])])


def draw_plot_legend(app, g: dict, cv, cw: int, ch: int, m: int, title: str, lines):
    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    NW = g["NW"]
    W = g["W"]
    s = PLOT_SETTINGS
    if not s.get("show_legend", True):
        return
    pos = s.get("legend_pos", "upper left")
    fw = "bold" if s.get("font_bold", True) else "normal"
    fs = max(8, int(s.get("font_size", 12)) - 3)

    pad = 8
    box_w = min(170, max(120, int((cw - 2 * m) * 0.22)))
    line_h = 16
    box_h = 18 + len(lines) * line_h

    if pos == "upper right":
        x1, y1 = cw - m - pad - box_w, m + pad
    elif pos == "lower left":
        x1, y1 = m + pad, ch - m - pad - box_h
    elif pos == "lower right":
        x1, y1 = cw - m - pad - box_w, ch - m - pad - box_h
    elif pos == "center":
        x1, y1 = (cw - box_w) // 2, (ch - box_h) // 2
    else:
        x1, y1 = m + pad, m + pad

    x2, y2 = x1 + box_w, y1 + box_h
    axc = s.get("axis_color", "#000000")
    bg = s.get("plot_bg", "#ffffff")
    cv.create_rectangle(x1, y1, x2, y2, fill=bg, outline=axc, width=1)
    if title:
        cv.create_text(x1 + 8, y1 + 8, text=title, fill=axc, font=("Helvetica", fs, "bold"), anchor=NW)
    yy = y1 + 22
    for lbl, col in lines:
        cv.create_oval(x1 + 8, yy - 4, x1 + 16, yy + 4, fill=col, outline=axc, width=1)
        cv.create_text(x1 + 22, yy, text=lbl, fill=axc, font=("Helvetica", fs, fw), anchor=W)
        yy += line_h


def create_professional_plot_template(app, g: dict, cv, cw: int, ch: int, m: int, title: str, xlabel: str, ylabel: str):
    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    s = PLOT_SETTINGS
    cv.create_rectangle(0, 0, cw, ch, fill=s["plot_bg"], outline="")
    cv.create_rectangle(m, m, cw - m, ch - m, outline=s["axis_color"], width=int(s["axis_width"]))
    fw = "bold" if s["font_bold"] else "normal"
    if title:
        cv.create_text(cw // 2, m // 2, text=title, fill=s["axis_color"], font=("Helvetica", s["font_size"] + 2, "bold"))
    xlabel_y = ch - max(14, int(s["font_size"] * 1.2))
    if xlabel:
        cv.create_text(cw // 2, xlabel_y, text=xlabel, fill=s["axis_color"], font=("Helvetica", s["font_size"], fw))
    if ylabel:
        cv.create_text(16, ch // 2, text=ylabel, fill=s["axis_color"], font=("Helvetica", s["font_size"], fw), angle=90)
    cv.create_line(m, ch - m, cw - m, ch - m, fill=s["axis_color"], width=s["axis_width"])
    cv.create_line(m, m, m, ch - m, fill=s["axis_color"], width=s["axis_width"])
    if s["show_grid"]:
        for i in range(1, s["n_factors"]):
            gy, gx = m + i * (ch - 2 * m) // s["n_factors"], m + i * (cw - 2 * m) // s["n_factors"]
            cv.create_line(m, gy, cw - m, gy, fill=s["grid_color"], width=s["grid_width"], dash=(3, 3))
            cv.create_line(gx, m, gx, ch - m, fill=s["grid_color"], width=s["grid_width"], dash=(3, 3))


def draw_histogram(app, g: dict, cv, cw: int, ch: int, m: int, data: dict):
    import math
    import random as _rnd

    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    E = g["E"]
    N = g["N"]

    vals = data.get("values", [])
    col = data.get("col_name", "")
    if not vals:
        draw_empty_state(app, g, cv, col or "")
        return
    style = PLOT_SETTINGS.get("dist_style", "Bars")
    bins_count = 15
    min_v, max_v = min(vals), max(vals)
    if max_v == min_v:
        max_v += 1
    bin_w = (max_v - min_v) / bins_count
    counts = [sum(1 for v in vals if min_v + i * bin_w <= v < min_v + (i + 1) * bin_w) for i in range(bins_count)]
    max_count_raw = max(counts) or 1
    max_count = max_count_raw * 1.18
    s = PLOT_SETTINGS
    fw = "bold" if s["font_bold"] else "normal"
    x_inset = 10
    plot_left = m + x_inset
    plot_right = cw - m - x_inset
    plot_w = max(1, plot_right - plot_left)

    if style == "Box":
        vals_sorted = sorted(vals)
        n = len(vals_sorted)

        def q(p):
            if n == 1:
                return vals_sorted[0]
            idx = int(round((n - 1) * p))
            return vals_sorted[max(0, min(n - 1, idx))]

        vmin, q1, med, q3, vmax = vals_sorted[0], q(0.25), q(0.5), q(0.75), vals_sorted[-1]
        x0 = plot_left + 30
        x1 = plot_right - 30
        y_mid = (m + (ch - m)) // 2

        def x_map(v):
            return x0 + (0 if vmax == vmin else (v - vmin) / (vmax - vmin) * (x1 - x0))

        cv.create_line(x_map(vmin), y_mid, x_map(vmax), y_mid, fill=s["axis_color"], width=2)
        cv.create_rectangle(x_map(q1), y_mid - 25, x_map(q3), y_mid + 25, outline=s["axis_color"], width=2, fill=s["plot_bg"])
        cv.create_line(x_map(med), y_mid - 25, x_map(med), y_mid + 25, fill=s["color_discard"], width=3)
        cv.create_line(x_map(vmin), y_mid - 10, x_map(vmin), y_mid + 10, fill=s["axis_color"], width=2)
        cv.create_line(x_map(vmax), y_mid - 10, x_map(vmax), y_mid + 10, fill=s["axis_color"], width=2)
    elif style == "Dots":
        vmin, vmax = min_v, max_v
        x0 = plot_left
        x1 = plot_right
        y0 = m + 20
        y1 = ch - m - 20
        rr = max(2, int(s.get("marker_size", 8) / 3))
        for v in vals:
            x = x0 + (0 if vmax == vmin else (v - vmin) / (vmax - vmin) * (x1 - x0))
            y = (y0 + y1) / 2 + _rnd.uniform(-0.35, 0.35) * (y1 - y0) / 2
            cv.create_oval(x - rr, y - rr, x + rr, y + rr, fill=s["color_ideal"], outline=s["axis_color"], width=1)
        if s.get("dots_axis_line", True):
            y_mid = (y0 + y1) / 2
            cv.create_line(x0, y_mid, x1, y_mid, fill=s["grid_color"], width=1)
    else:
        for i, c in enumerate(counts):
            x1 = plot_left + i * (plot_w) / bins_count
            x2 = plot_left + (i + 1) * (plot_w) / bins_count
            h = (c / max_count) * (ch - 2 * m)
            cv.create_rectangle(x1 + 1, ch - m - h, x2 - 1, ch - m, fill=s["color_ideal"], outline=s["axis_color"], width=1)
        if s.get("show_gaussian", False) and len(vals) >= 5:
            try:
                mean = sum(vals) / len(vals)
                var = sum((v - mean) ** 2 for v in vals) / max(1, (len(vals) - 1))
                sd = var**0.5 if var > 0 else 1e-6
                pts = []
                steps = 80
                for j in range(steps + 1):
                    x_val = min_v + (max_v - min_v) * j / steps
                    y_pdf = (1.0 / (sd * (2 * math.pi) ** 0.5)) * math.exp(-0.5 * ((x_val - mean) / sd) ** 2)
                    y_scaled = len(vals) * bin_w * y_pdf
                    x = plot_left + (0 if max_v == min_v else (x_val - min_v) / (max_v - min_v) * plot_w)
                    y = ch - m - (y_scaled / max_count) * (ch - 2 * m)
                    y = max(m, min(ch - m, y))
                    pts.append((x, y))
                for (x_a, y_a), (x_b, y_b) in zip(pts, pts[1:]):
                    cv.create_line(x_a, y_a, x_b, y_b, fill=s["color_discard"], width=2)
            except Exception:
                pass

    for i in range(s["n_factors"] + 1):
        y = m + i * (ch - 2 * m) // s["n_factors"]
        cv.create_text(m - 22, y, text=str(int(max_count_raw - (max_count_raw / s["n_factors"]) * i)), fill=s["axis_color"], font=("Helvetica", s["font_size"] - 1, fw), anchor=E)
        xt = plot_left + i * (plot_w) / s["n_factors"]
        xt = max(plot_left, min(plot_right, xt))
        tick_y = (ch - m) + max(6, int(s["font_size"] * 0.55))
        cv.create_text(xt, tick_y, text=str(round(min_v + (max_v - min_v) / s["n_factors"] * i, 3)), fill=s["axis_color"], font=("Helvetica", s["font_size"] - 1, fw), anchor=N)

    es = app.lang_var.get() == "Español"
    leg_title = "Leyenda" if es else "Legend"
    if style == "Box":
        leg_lines = [
            ("Bigote (mín–máx)" if es else "Whisker (min–max)", s["axis_color"]),
            ("Caja (Q1–Q3)" if es else "Box (Q1–Q3)", s["plot_bg"]),
            ("Mediana" if es else "Median", s["color_discard"]),
        ]
    elif style == "Dots":
        leg_lines = [("Valores" if es else "Values", s["color_ideal"])]
    else:
        leg_lines = [("Histograma" if es else "Histogram", s["color_ideal"])]
        if s.get("show_gaussian", False) and len(vals) >= 5:
            leg_lines.append(("Ajuste normal" if es else "Normal fit", s["color_discard"]))
    draw_plot_legend(app, g, cv, cw, ch, m, leg_title, leg_lines)


def draw_class_hist(app, g: dict, cv, cw: int, ch: int, m: int, data: dict):
    PLOT_SETTINGS = g["PLOT_SETTINGS"]
    ideal = data.get("ideal", [])
    discard = data.get("discard", [])
    all_vals = ideal + discard
    if not all_vals:
        draw_empty_state(app, g, cv, "")
        return
    bins_count = 10
    min_v, max_v = min(all_vals), max(all_vals)
    bin_w = (max_v - min_v) / bins_count if max_v != min_v else 1.0
    i_counts = [sum(1 for v in ideal if min_v + i * bin_w <= v < min_v + (i + 1) * bin_w) for i in range(bins_count)]
    d_counts = [sum(1 for v in discard if min_v + i * bin_w <= v < min_v + (i + 1) * bin_w) for i in range(bins_count)]
    max_count = max(max(i_counts) or 1, max(d_counts) or 1)
    s = PLOT_SETTINGS
    w = (cw - 2 * m) / bins_count
    for i in range(bins_count):
        x1 = m + i * w
        h_i = (i_counts[i] / max_count) * (ch - 2 * m)
        h_d = (d_counts[i] / max_count) * (ch - 2 * m)
        cv.create_rectangle(x1 + 1, ch - m - h_i, x1 + w / 2 - 2, ch - m, fill=s["color_ideal"], outline=s["axis_color"], width=1)
        cv.create_rectangle(x1 + w / 2 + 1, ch - m - h_d, x1 + w - 1, ch - m, fill=s["color_discard"], outline=s["axis_color"], width=1)
    leg_title = "Leyenda" if app.lang_var.get() == "Español" else "Legend"
    draw_plot_legend(app, g, cv, cw, ch, m, leg_title, [(app.t("ideal"), s["color_ideal"]), (app.t("descartado"), s["color_discard"])])

