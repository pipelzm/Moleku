from __future__ import annotations

import os
import sys


def export_plots_paper_ready(
    folder: str,
    *,
    plot_canvases,
    prepare_plot_data,
    get_xlabel,
    t,
    filter_value: str,
    lang_value: str,
    plot_settings: dict,
    Chem=None,
):
    """
    Export current plots as publication-ready figures.

    Parameters are injected so this module does not depend on the GUI class.
    """
    import json
    import datetime as _dt
    import platform as _platform

    try:
        import numpy as _np
    except Exception as ex:
        raise RuntimeError(f"Missing dependency: {ex}") from ex

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        raise RuntimeError(
            "High-quality plot export requires matplotlib.\n\nInstall:\n  pip install matplotlib"
        )

    os.makedirs(folder, exist_ok=True)

    dpi = int(plot_settings.get("dpi", 300) or 300)
    bins = int(plot_settings.get("hist_bins", 30) or 30)
    bins = max(5, min(200, bins))
    fig_w = float(plot_settings.get("export_fig_w_in", 3.35) or 3.35)
    fig_h = float(plot_settings.get("export_fig_h_in", 2.35) or 2.35)
    font_family = str(plot_settings.get("font_family", "DejaVu Sans") or "DejaVu Sans")

    plt.rcParams.update({
        "font.family": font_family,
        "font.size": max(7, int(plot_settings.get("font_size", 8) or 8)),
        "axes.titlesize": max(8, int(plot_settings.get("font_size", 8) or 8) + 1),
        "axes.labelsize": max(7, int(plot_settings.get("font_size", 8) or 8)),
        "axes.linewidth": float(plot_settings.get("axis_width", 1.0) or 1.0),
        "xtick.labelsize": max(7, int(plot_settings.get("font_size", 8) or 8) - 1),
        "ytick.labelsize": max(7, int(plot_settings.get("font_size", 8) or 8) - 1),
        "savefig.dpi": dpi,
    })

    exports = []
    for idx, (_cv, key) in enumerate(plot_canvases, start=1):
        data = prepare_plot_data(key)
        if not data:
            continue

        safe_key = key.replace(" ", "_").replace("/", "_")
        base = os.path.join(folder, f"plot_{idx:02d}_{safe_key}")

        fig = plt.figure(figsize=(fig_w, fig_h), dpi=dpi)
        ax = fig.add_subplot(111)

        ax.set_facecolor(plot_settings.get("plot_bg", "#ffffff"))
        for spine in ax.spines.values():
            spine.set_color(plot_settings.get("axis_color", "#000000"))
            spine.set_linewidth(float(plot_settings.get("axis_width", 2.5)))
        try:
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
        except Exception:
            pass
        ax.tick_params(colors=plot_settings.get("axis_color", "#000000"), width=float(plot_settings.get("axis_width", 2.5)))
        if plot_settings.get("show_grid", True):
            ax.grid(True, color=plot_settings.get("grid_color", "#e0e0e0"), linewidth=float(plot_settings.get("grid_width", 0.5)), alpha=0.9)

        ax.set_title(key, fontweight="bold" if plot_settings.get("font_bold", False) else "normal")

        coords_path = None
        if key.endswith("Distribution"):
            vals = _np.asarray(data.get("values", []), dtype=float)
            vals = vals[_np.isfinite(vals)]
            if vals.size == 0:
                plt.close(fig)
                continue
            ax.hist(vals, bins=bins, color=plot_settings.get("color_ideal", "#27ae60"), edgecolor=plot_settings.get("axis_color", "#000000"), linewidth=0.8)
            ax.set_ylabel("Frequency")
            ax.set_xlabel(get_xlabel(key))
            ax.text(0.99, 0.97, f"n={vals.size}", transform=ax.transAxes, ha="right", va="top", fontsize=10, color=plot_settings.get("axis_color", "#000000"))

        elif key.endswith("by Classification"):
            ideal = _np.asarray(data.get("ideal", []), dtype=float)
            discard = _np.asarray(data.get("discard", []), dtype=float)
            ideal = ideal[_np.isfinite(ideal)]
            discard = discard[_np.isfinite(discard)]
            if ideal.size + discard.size == 0:
                plt.close(fig)
                continue
            allv = _np.concatenate([ideal, discard]) if discard.size else ideal
            edges = _np.histogram_bin_edges(allv, bins=bins)
            ax.hist(ideal, bins=edges, density=True, alpha=0.75, label=t("ideal"), color=plot_settings.get("color_ideal", "#27ae60"))
            ax.hist(discard, bins=edges, density=True, alpha=0.65, label=t("descartado"), color=plot_settings.get("color_discard", "#c0392b"))
            ax.set_ylabel("Density")
            ax.set_xlabel(get_xlabel(key))
            if plot_settings.get("show_legend", True):
                ax.legend(loc="upper right", frameon=False)

        elif key.startswith("2D PCA"):
            pts = data.get("points", [])
            if not pts:
                plt.close(fig)
                continue
            xs = _np.asarray([p[0] for p in pts], dtype=float)
            ys = _np.asarray([p[1] for p in pts], dtype=float)
            is_ideal = _np.asarray([bool(p[2]) for p in pts], dtype=bool)
            ax.scatter(xs[~is_ideal], ys[~is_ideal], s=10, alpha=0.65, c=plot_settings.get("color_discard", "#c0392b"), label=t("descartado"))
            ax.scatter(xs[is_ideal], ys[is_ideal], s=12, alpha=0.75, c=plot_settings.get("color_ideal", "#27ae60"), label=t("ideal"))
            ax.set_xlabel("PC1")
            ax.set_ylabel("PC2")
            if plot_settings.get("show_legend", True):
                ax.legend(loc="upper right", frameon=False)
            # Export coordinates
            coords_path = base + "_coords.csv"
            try:
                import csv as _csv
                with open(coords_path, "w", newline="", encoding="utf-8") as f:
                    w = _csv.writer(f)
                    w.writerow(["PC1", "PC2", "Classification"])
                    for x, y, ok in pts:
                        w.writerow([x, y, "Ideal" if ok else "Discarded"])
            except Exception:
                coords_path = None

        fig.tight_layout()
        png_path = base + ".png"
        pdf_path = base + ".pdf"
        svg_path = base + ".svg"
        fig.savefig(png_path, dpi=dpi, bbox_inches="tight")
        try:
            fig.savefig(pdf_path, bbox_inches="tight")
            fig.savefig(svg_path, bbox_inches="tight")
        except Exception:
            pass
        plt.close(fig)

        exports.append(
            {
                "key": key,
                "files": [p for p in [png_path, pdf_path, svg_path] if os.path.exists(p)],
                "coords": [p for p in [coords_path] if p and os.path.exists(p)],
                "bins": bins,
                "dpi": dpi,
                "filter": filter_value,
                "lang": lang_value,
            }
        )

    manifest = {
        "tool": "Moleku",
        "export_type": "paper_ready_plots",
        "created_utc": _dt.datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
        "plot_settings": dict(plot_settings),
        "plots": exports,
        "environment": {
            "python": sys.version.split()[0],
            "platform": _platform.platform(),
        },
    }
    try:
        import matplotlib as _mpl
        manifest["environment"]["matplotlib"] = getattr(_mpl, "__version__", "unknown")
    except Exception:
        pass
    try:
        manifest["environment"]["rdkit"] = getattr(Chem, "__version__", "unknown") if Chem else "unavailable"
    except Exception:
        pass

    with open(os.path.join(folder, "plots_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

