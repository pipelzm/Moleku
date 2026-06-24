#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Moleku — Multi Component Reaction Generator
=================================================
Desktop GUI for virtual library generation via Multi-Component Reactions.
Developed by Felipe Lizama Mora · SB&BCS Lab - UFRO

Note: The Python package/module names (`mcrg`, `mcrg_desktop`, `MCRGApp`) are kept
for backwards compatibility with imports and tests. Only the user-facing
brand and the packaged executable use the new "Moleku" name.
"""
import os, sys, io, itertools, zipfile, threading, math, webbrowser, random, time
from pathlib import Path
from collections import defaultdict
# ── TKINTER ──────────────────────────────────────────────
try:
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog, colorchooser
    from tkinter import ttk
    from tkinter import (END, DISABLED, NORMAL, BOTH, LEFT, RIGHT,
                         TOP, BOTTOM, X, Y, W, E, N, S, NW,
                         HORIZONTAL, VERTICAL, CENTER, WORD, FLAT,
                         StringVar, BooleanVar, DoubleVar, IntVar)
    _TK_READY = True
except Exception:
    tk = None
    filedialog = messagebox = simpledialog = colorchooser = None
    ttk = None
    END = "end"; DISABLED = "disabled"; NORMAL = "normal"
    BOTH = "both"; LEFT = "left"; RIGHT = "right"
    TOP = "top"; BOTTOM = "bottom"; X = "x"; Y = "y"
    W = "w"; E = "e"; N = "n"; S = "s"; NW = "nw"
    HORIZONTAL = "horizontal"; VERTICAL = "vertical"; CENTER = "center"; WORD = "word"; FLAT = "flat"
    StringVar = BooleanVar = DoubleVar = IntVar = None
    _TK_READY = False
try:
    import customtkinter as ctk
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    HAS_CTK = True
except ImportError:
    HAS_CTK = False

# ── Deferred heavy imports ──────────────────────────────────────────
_CHEM_READY = False
Chem = AllChem = Descriptors = Lipinski = Draw = None
pd = None
Image = ImageTk = None

# Modularized helpers (keep mcrg_desktop.py as entrypoint and re-export API)
try:
    from mcrg.loaders import cargar_dataframe as _cargar_dataframe_mod
    from mcrg.loaders import cargar_dataframe_with_report as _cargar_dataframe_with_report_mod
except Exception:
    _cargar_dataframe_mod = None
    _cargar_dataframe_with_report_mod = None

try:
    from mcrg.smiles_utils import parse_smiles_flexible as _parse_smiles_flexible_mod
except Exception:
    _parse_smiles_flexible_mod = None

try:
    from mcrg.i18n import LOCALES, PLOT_DESC, display_component_name, display_core_reagent_name
except Exception:
    LOCALES = {}
    PLOT_DESC = {}
    def display_component_name(comp: str, lang: str) -> str:  # type: ignore
        return comp
    def display_core_reagent_name(name: str, lang: str) -> str:  # type: ignore
        return name

try:
    from mcrg.engine import run_mcr as _run_mcr_mod
except Exception:
    _run_mcr_mod = None

try:
    from mcrg.runtime_monitor import dependency_status as _dependency_status_mod
    from mcrg.runtime_monitor import sample_usage as _sample_usage_mod
except Exception:
    _dependency_status_mod = None
    _sample_usage_mod = None

try:
    from mcrg.catalog import MCR_CATALOGO as _MCR_CATALOGO_MOD
except Exception:
    _MCR_CATALOGO_MOD = None

try:
    from mcrg.plots import export_plots_paper_ready as _export_plots_paper_ready_mod
except Exception:
    _export_plots_paper_ready_mod = None

try:
    from mcrg.exports import export_paper_dataset_zip as _export_paper_dataset_zip_mod
    from mcrg.exports import export_research_bundle_zip as _export_research_bundle_zip_mod
except Exception:
    _export_paper_dataset_zip_mod = None
    _export_research_bundle_zip_mod = None

try:
    from mcrg.ui_motor import build_motor as _build_motor_mod
    from mcrg.ui_results import build_results as _build_results_mod
    from mcrg.ui_admet_tab import build_admet as _build_admet_mod
    from mcrg.ui_space import build_space as _build_space_mod
    from mcrg.ui_guide import build_guide as _build_guide_mod
    from mcrg.ui_about import build_about as _build_about_mod
except Exception:
    _build_motor_mod = None
    _build_results_mod = None
    _build_admet_mod = None
    _build_space_mod = None
    _build_guide_mod = None
    _build_about_mod = None

try:
    from mcrg.ui_dialogs import show_plot_settings as _show_plot_settings_mod
    from mcrg.ui_dialogs import show_table_columns_dialog as _show_table_columns_dialog_mod
    from mcrg.ui_dialogs import show_custom_zip_dialog as _show_custom_zip_dialog_mod
except Exception:
    _show_plot_settings_mod = None
    _show_table_columns_dialog_mod = None
    _show_custom_zip_dialog_mod = None

try:
    from mcrg.ui_admet import admet_copy_selected_smiles as _admet_copy_selected_smiles_mod
    from mcrg.ui_admet import admet_copy_ideal_smiles as _admet_copy_ideal_smiles_mod
    from mcrg.ui_admet import admet_open_web as _admet_open_web_mod
    from mcrg.ui_admet import admet_predict_selected_local as _admet_predict_selected_local_mod
    from mcrg.ui_admet import admet_predict_visible_local as _admet_predict_visible_local_mod
    from mcrg.ui_admet import admet_predict_ideal_local as _admet_predict_ideal_local_mod
    from mcrg.ui_admet import admet_predict_results_local as _admet_predict_results_local_mod
    from mcrg.ui_admet import admet_predict_pasted_local as _admet_predict_pasted_local_mod
    from mcrg.ui_admet import show_admet_predictions as _show_admet_predictions_mod
except Exception:
    _admet_copy_selected_smiles_mod = None
    _admet_copy_ideal_smiles_mod = None
    _admet_open_web_mod = None
    _admet_predict_selected_local_mod = None
    _admet_predict_visible_local_mod = None
    _admet_predict_ideal_local_mod = None
    _admet_predict_results_local_mod = None
    _admet_predict_pasted_local_mod = None
    _show_admet_predictions_mod = None

try:
    from mcrg.ui_admet_tab import apply_admet_filter as _apply_admet_filter_mod
    from mcrg.ui_admet_tab import sort_admet_tree as _sort_admet_tree_mod
    from mcrg.ui_admet_tab import on_admet_select as _on_admet_select_mod
    from mcrg.ui_admet_tab import refresh_admet_labels as _refresh_admet_labels_mod
    from mcrg.ui_admet_tab import clear_admet_view as _clear_admet_view_mod
    from mcrg.ui_admet_tab import export_admet_csv as _export_admet_csv_mod
except Exception:
    _apply_admet_filter_mod = None
    _sort_admet_tree_mod = None
    _on_admet_select_mod = None
    _refresh_admet_labels_mod = None
    _clear_admet_view_mod = None
    _export_admet_csv_mod = None

try:
    from mcrg.plot_canvas import render_espacio as _render_espacio_mod
    from mcrg.plot_canvas import draw_plots as _draw_plots_mod
    from mcrg.plot_canvas import prepare_plot_data as _prepare_plot_data_mod
    from mcrg.plot_canvas import draw_empty_state as _draw_empty_state_mod
    from mcrg.plot_canvas import render_from_cache as _render_from_cache_mod
    from mcrg.plot_canvas import draw_single_plot as _draw_single_plot_mod
    from mcrg.plot_canvas import draw_embedding_2d as _draw_embedding_2d_mod
    from mcrg.plot_canvas import draw_plot_legend as _draw_plot_legend_mod
    from mcrg.plot_canvas import create_professional_plot_template as _create_professional_plot_template_mod
    from mcrg.plot_canvas import draw_histogram as _draw_histogram_mod
    from mcrg.plot_canvas import draw_class_hist as _draw_class_hist_mod
    from mcrg.plot_canvas import get_xlabel as _get_xlabel_mod
    from mcrg.plot_canvas import get_ylabel as _get_ylabel_mod
except Exception:
    _render_espacio_mod = None
    _draw_plots_mod = None
    _prepare_plot_data_mod = None
    _draw_empty_state_mod = None
    _render_from_cache_mod = None
    _draw_single_plot_mod = None
    _draw_embedding_2d_mod = None
    _draw_plot_legend_mod = None
    _create_professional_plot_template_mod = None
    _draw_histogram_mod = None
    _draw_class_hist_mod = None
    _get_xlabel_mod = None
    _get_ylabel_mod = None

try:
    from mcrg.ui_preview import update_preview as _update_preview_mod
    from mcrg.ui_preview import schedule_preview_redraw as _schedule_preview_redraw_mod
except Exception:
    _update_preview_mod = None
    _schedule_preview_redraw_mod = None

try:
    from mcrg.ui_table import apply_filter as _apply_filter_mod
    from mcrg.ui_table import sort_tree as _sort_tree_mod
    from mcrg.ui_table import on_tree_select as _on_tree_select_mod
except Exception:
    _apply_filter_mod = None
    _sort_tree_mod = None
    _on_tree_select_mod = None

try:
    from mcrg.ui_motor_slots import refresh_slots as _refresh_slots_mod
    from mcrg.ui_motor_slots import clear_motor_inputs as _clear_motor_inputs_mod
    from mcrg.ui_motor_slots import browse_file as _browse_file_mod
except Exception:
    _refresh_slots_mod = None
    _clear_motor_inputs_mod = None
    _browse_file_mod = None

try:
    from mcrg.ui_run import run_clicked as _run_clicked_mod
except Exception:
    _run_clicked_mod = None

try:
    from mcrg.export_pdf import export_pdf as _export_pdf_mod
except Exception:
    _export_pdf_mod = None

try:
    from mcrg.ui_exports_simple import export_file as _export_file_mod
    from mcrg.ui_exports_simple import exp_csv as _exp_csv_mod
    from mcrg.ui_exports_simple import exp_xlsx as _exp_xlsx_mod
    from mcrg.ui_exports_simple import exp_pdf as _exp_pdf_mod
    from mcrg.ui_exports_simple import exp_table as _exp_table_mod
except Exception:
    _export_file_mod = None
    _exp_csv_mod = None
    _exp_xlsx_mod = None
    _exp_pdf_mod = None
    _exp_table_mod = None

try:
    from mcrg.ui_results_helpers import clear_results as _clear_results_mod
    from mcrg.ui_results_helpers import update_results_counter as _update_results_counter_mod
    from mcrg.ui_results_helpers import refresh_results_help_panels as _refresh_results_help_panels_mod
    from mcrg.ui_results_helpers import apply_results_info_layout as _apply_results_info_layout_mod
    from mcrg.ui_results_helpers import toggle_results_info_panels as _toggle_results_info_panels_mod
except Exception:
    _clear_results_mod = None
    _update_results_counter_mod = None
    _refresh_results_help_panels_mod = None
    _apply_results_info_layout_mod = None
    _toggle_results_info_panels_mod = None

try:
    from mcrg.ui_app_actions import restart_app as _restart_app_mod
    from mcrg.ui_app_actions import download_example as _download_example_mod
    from mcrg.ui_app_actions import download_example_pack as _download_example_pack_mod
    from mcrg.ui_app_actions import open_feedback as _open_feedback_mod
except Exception:
    _restart_app_mod = None
    _download_example_mod = None
    _download_example_pack_mod = None
    _open_feedback_mod = None

try:
    from mcrg.ui_nav_i18n import make_hyperlink as _make_hyperlink_mod
    from mcrg.ui_nav_i18n import switch_tab as _switch_tab_mod
    from mcrg.ui_nav_i18n import on_lang_change as _on_lang_change_mod
    from mcrg.ui_nav_i18n import update_labels as _update_labels_mod
except Exception:
    _make_hyperlink_mod = None
    _switch_tab_mod = None
    _on_lang_change_mod = None
    _update_labels_mod = None

try:
    from mcrg.ui_table_headings import refresh_table_headings as _refresh_table_headings_mod
except Exception:
    _refresh_table_headings_mod = None

try:
    from mcrg.ui_export_3d import exp_zip_3d as _exp_zip_3d_mod
except Exception:
    _exp_zip_3d_mod = None

try:
    from mcrg.ui_exports_heavy import exp_bundle as _exp_bundle_mod
    from mcrg.ui_exports_heavy import exp_paper as _exp_paper_mod
except Exception:
    _exp_bundle_mod = None
    _exp_paper_mod = None

try:
    from mcrg.ui_export_wiring import export_paper_dataset_zip as _export_paper_dataset_zip_wiring_mod
    from mcrg.ui_export_wiring import export_research_bundle_zip as _export_research_bundle_zip_wiring_mod
except Exception:
    _export_paper_dataset_zip_wiring_mod = None
    _export_research_bundle_zip_wiring_mod = None

try:
    from mcrg.ui_clipboard_helpers import get_selected_smiles as _get_selected_smiles_mod
    from mcrg.ui_clipboard_helpers import get_ideal_smiles as _get_ideal_smiles_mod
    from mcrg.ui_clipboard_helpers import copy_to_clipboard as _copy_to_clipboard_mod
except Exception:
    _get_selected_smiles_mod = None
    _get_ideal_smiles_mod = None
    _copy_to_clipboard_mod = None

try:
    from mcrg.ui_common import col_label as _col_label_mod
    from mcrg.ui_common import get_font as _get_font_mod
    from mcrg.ui_common import btn as _btn_mod
    from mcrg.ui_common import lbl as _lbl_mod
    from mcrg.ui_common import frame as _frame_mod
    from mcrg.ui_common import build_ui as _build_ui_mod
    _ui_common_import_error = None
except Exception as _e:
    _ui_common_import_error = repr(_e)
    _col_label_mod = None
    _get_font_mod = None
    _btn_mod = None
    _lbl_mod = None
    _frame_mod = None
    _build_ui_mod = None

def _load_heavy():
    global Chem, AllChem, Descriptors, Lipinski, Draw, _CHEM_READY, pd, Image, ImageTk
    try: import pandas as _pd; pd = _pd
    except ImportError: pass
    try: from PIL import Image as _Im, ImageTk as _ImTk; Image, ImageTk = _Im, _ImTk
    except ImportError: pass
    try:
        from rdkit import Chem as _C, RDLogger
        from rdkit.Chem import AllChem as _A, Descriptors as _D, Lipinski as _L, Draw as _Dr
        RDLogger.DisableLog('rdApp.*')
        Chem, AllChem, Descriptors, Lipinski, Draw = _C, _A, _D, _L, _Dr
        _CHEM_READY = True
    except ImportError: _CHEM_READY = False

# ════════════════════════════════════════════════════════════════════════
# COLOURS & PLOT SETTINGS
# ════════════════════════════════════════════════════════════════════════
CL = {
    "bg": "#1e1e1e", "bg2": "#2b2b2b", "bg3": "#333333",
    "fg": "#d4d4d4", "dim": "#808080", "accent": "#e87a20",
    "accent2": "#c46a1a", "info": "#4fc3f7", "ideal": "#27ae60",
    "warning": "#d4a017", "discard": "#c0392b", "entry": "#3c3c3c", "border": "#555555",
    "grid": "#3a3a3a", "link": "#e87a20",
    "plot_bg": "#ffffff", "plot_fg": "#000000", "plot_border": "#000000"
}

PLOT_SETTINGS = {
    "color_ideal": "#27ae60", "color_warning": "#d4a017", "color_discard": "#c0392b",
    "axis_color": "#000000", "grid_color": "#e0e0e0", "plot_bg": "#ffffff",
    "font_size": 12, "font_bold": True, "marker_size": 8,
    "line_width": 2.0, "axis_width": 2.5, "grid_width": 0.5,
    "show_grid": True, "show_legend": True, "legend_pos": "upper left",
    "n_factors": 5, "dpi": 300,
    # Export / histogram determinism
    "hist_bins": 30,
    # Publication export defaults (single-column friendly)
    "export_fig_w_in": 3.35,   # ~85 mm
    "export_fig_h_in": 2.35,   # balanced for single-column
    "font_family": "DejaVu Sans",
    # Chemical Space plot options
    "dist_style": "Bars",          # Bars | Dots | Box
    "show_gaussian": False,        # overlay Gaussian curve (Histogram only)
    "dots_axis_line": True,        # show baseline/axis line for dot plots
}

# ════════════════════════════════════════════════════════════════════════
# REACTION PREVIEW IMAGES
# ════════════════════════════════════════════════════════════════════════
REACTION_PREVIEW_IMAGES = {
    "Biginelli (3-CR)": "images/biginelli_reaction.png",
    "Bucherer-Bergs (4-CR)": "images/bucherer_reaction.png", 
    "Gewald (3-CR)": "images/gewald_reaction.png",
    "GBB (3-CR)": "images/gbb_reaction.png",
    "Doebner (3-CR)": "images/doebner_reaction.png",
    "Passerini (3-CR)": "images/passerini_reaction.png",
    "Mannich (3-CR)": "images/mannich_reaction.png",
    "Strecker (3-CR)": "images/strecker_reaction.png",
    "Petasis (3-CR)": "images/petasis_reaction.png",
    "Kabachnik-Fields (3-CR)": "images/kabachnik_reaction.png",
    "Hantzsch (3-CR)": "images/hantzsch_reaction.png",
    "Ugi (4-CR)": "images/ugi_reaction.png",
    "Ugi-Smiles (4-CR)": "images/ugi_smiles_reaction.png",
    "Asinger (4-CR)": "images/asinger_reaction.png",
}

PREVIEW_CANVAS_HEIGHT = 240

def resource_path(relative_path: str) -> str:
    """
    Resolve a file path relative to the app/script location.
    Works for normal execution and common bundlers (e.g., PyInstaller).
    """
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return str((base / relative_path).resolve())

# ════════════════════════════════════════════════════════════════════════
# MCR CATALOGUE (Updated with requested central reagents)
# ════════════════════════════════════════════════════════════════════════
MCR_CATALOGO = {
    "Biginelli (3-CR)": {
        "componentes": ["Aldehídos", "Beta-Cetoésteres"],
        "smarts": '[*:1][CH1:2]=[O:3].[NH2:4][C:5](=[O,S,N:6])[NH2:7].[*:8][C:9](=[O:10])[CH2:11][C:12](=[O:13])[O:14][*:15]>>[*:1][CH1:2]1[NH:7][C:5](=[O,S,N:6])[NH:4][C:9]([*:8])=[C:11]1[C:12](=[O:13])[O:14][*:15]',
        "opciones_centrales": {"Urea": "[NH2]C(=O)[NH2]", "Tiourea": "[NH2]C(=S)[NH2]", "Guanidina": "[NH2]C(=[NH])[NH2]"},
        "producto_ejemplo": "Cc1c(C(=O)OC)nc(C)nc1O",
        "doi": "10.3390/ph15081009",
        "info_es": "Síntesis de dihidropirimidinonas (DHPM). Catalizada por ácidos de Lewis o Brønsted.",
        "info_en": "Synthesis of Dihydropyrimidinones (DHPMs). Catalyzed by Lewis/Brønsted acids."
    },
    "Passerini (3-CR)": {
        "componentes": ["Aldehídos/Cetonas", "Ácidos Carboxílicos", "Isocianuros"],
        "smarts": '[C:1]=[O:2].[O:3]=[C:4][OH:5].[C-:6]#[N+:7][C:8]>>[C:1]([O:5][C:4]=[O:3])([C:6](=[O:2])[NH:7][C:8])',
        "producto_ejemplo": "CC(=O)NC(c1ccccc1)C(=O)OC",
        "doi": "10.3762/bjoc.20.261",
        "info_es": "Formación de α-aciloxiamidas. Requiere condiciones suaves (sin catalizador).",
        "info_en": "Formation of α-acyloxyamides. Requires mild conditions (catalyst-free)."
    },
    "Mannich (3-CR)": {
        "componentes": ["Aldehídos", "Aminas Sec/Prim", "Carbonilos Enolizables"],
        "smarts": '[C:1]=[O:2].[N:3]([H]).[C:4](=[O:5])[CH1,CH2,CH3:6]>>[N:3][C:1][C:6][C:4](=[O:5])',
        "producto_ejemplo": "CC(=O)CC(=O)NCc1ccccc1",
        "doi": "10.3390/ph15081009",
        "info_es": "Reacción clásica para obtener β-aminocetonas (bases de Mannich).",
        "info_en": "Classic reaction for β-aminoketones (Mannich bases)."
    },
    "Strecker (3-CR)": {
        "componentes": ["Aldehídos/Cetonas", "Aminas"],
        "smarts": '[C:1]=[O:2].[N:3]([H]).[C-:4]#[N:5]>>[N:3][C:1][C:4]#[N:5]',
        "opciones_centrales": {"Cianuro (HCN/KCN)": "[C-]#[N]"},
        "producto_ejemplo": "CC(C#N)NCc1ccccc1",
        "doi": "10.3390/ph15081009",
        "info_es": "Síntesis de α-aminonitrilos, precursores directos de α-aminoácidos.",
        "info_en": "Synthesis of α-aminonitriles, direct precursors to α-amino acids."
    },
    "Petasis (3-CR)": {
        "componentes": ["Aldehídos", "Aminas", "Ácidos Borónicos"],
        "smarts": '[C:1]=[O:2].[N:3]([H]).[B:4]([OH])([OH])[C:5]=[C:6]>>[N:3][C:1][C:5]=[C:6]',
        "producto_ejemplo": "C=CCNc1ccccc1",
        "doi": "10.3390/ph15081009",
        "info_es": "Aminación reductiva usando ácidos borónicos. Alta tolerancia funcional.",
        "info_en": "Reductive amination using boronic acids. High functional group tolerance."
    },
    "Kabachnik-Fields (3-CR)": {
        "componentes": ["Aldehídos/Cetonas", "Aminas", "Fosfitos Dialquílicos"],
        "smarts": '[C:1]=[O:2].[N:3]([H]).[P:4](=[O:5])([O:6])([O:7])[H]>>[N:3][C:1][P:4](=[O:5])([O:6])([O:7])',
        "producto_ejemplo": "CCO[P@](=O)(OCC)NC(c1ccccc1)c2ccccc2",
        "doi": "10.3390/ph15081009",
        "info_es": "Síntesis de α-aminofosfonatos (análogos de aminoácidos con fósforo).",
        "info_en": "Synthesis of α-aminophosphonates (phosphorus-containing amino acid analogs)."
    },
    "GBB (3-CR)": {
        "componentes": ["Aldehídos", "Isocianuros", "2-Aminoazinas"],
        "smarts": '[C:1]=[O:2].[C-:3]#[N+:4][C:5].[n:6]1[c,n:7][c,n:8][c,n:9][c,n:10][c:11]1[NH2:12]>>[C:5][N+0H:4][c+0:3]1[c:1][n+0:12][c:11]2[c,n:10][c,n:9][c,n:8][c,n:7][n+0:6]21',
        "producto_ejemplo": "CC(C)(C)Nc1c(-c2ccccc2)nc2ccccn12",
        "doi": "10.3390/ph15081009",
        "info_es": "Síntesis de imidazo[1,2-a]piridinas. Estructuras presentes en el fármaco Zolpidem.",
        "info_en": "Synthesis of imidazo[1,2-a]pyridines. Structures present in the drug Zolpidem."
    },
    "Doebner (3-CR)": {
        "componentes": ["Anilinas", "Aldehídos"],
        "smarts": '[c:1]1[c:2][c:3][c:4][c:5][c:6]1[NH2:7].[C:8]=[O:9].[C:10](=[O:11])([C:12])[C:13](=[O:14])[OH:15]>>[c:1]1[c:2][c:3][c:4][c:5][c:6]21[N:7]=[C:8][C:12]=[C:10]2[C:13](=[O:14])[OH:15]',
        "opciones_centrales": {"Ácido pirúvico": "CC(=O)C(=O)O"},
        "producto_ejemplo": "CC(=O)c1c(C)c2ccccc2n1c3ccccc3",
        "doi": "10.3390/ph15081009",
        "info_es": "Modificación de la quinolina de Hantzsch. Produce ácidos cinconínicos.",
        "info_en": "Modification of the Hantzsch quinoline. Produces cinchoninic acids."
    },
    "Gewald (3-CR)": {
        "componentes": ["Cetonas", "Alfa-Cianoésteres"],
        "smarts": '[C;H1,H2,H3:1][C:2]=[O:3].[C:4](#N)[C;H1,H2:5][C:6](=[O:7])[O:8].[S:9]>>[c+0:1]1[c+0:2][s+0:9][c+0:4]([N+0H2])[c+0:5]1[C:6](=[O:7])[O:8]',
        "smarts_variants": [
            "[C;H1,H2,H3:1][C:2]=[O:3].[C:4](#N)[CH2:5][C:6]#N.[S:9]>>[c+0:1]1[c+0:2][s+0:9][c+0:4]([N+0H2])[c+0:5]1[C:6]#N",
        ],
        "opciones_centrales": {"Azufre (S8)": "[S]"},
        "producto_ejemplo": "CCOC(=O)c1cc(C)sc1N",
        "doi": "10.3390/ph15081009",
        "info_es": "Síntesis de 2-aminotiofenos trisustituidos. Núcleo heterocíclico clave.",
        "info_en": "Synthesis of trisubstituted 2-aminothiophenes. Key heterocyclic nucleus."
    },
    "Hantzsch (3-CR)": {
        "componentes": ["Aldehídos", "Beta-Cetoéster (Equiv 1)", "Beta-Cetoéster (Equiv 2)"],
        "smarts": '[C:1]=[O:2].[C:3](=[O:4])[CH2:5][C:6](=[O:7])[O:8].[C:9](=[O:10])[CH:11]=[C:12]([NH2:13])[O:14]>>[C:1]1[C:5]([C:3]=[O:4])=[C:6]([O:8])[NH:13][C:12]([O:14])=[C:11]1[C:9]=[O:10]',
        "producto_ejemplo": "CC1=C(C(=O)OCC)NC(C)=C(C(=O)OC)C1c2ccccc2",
        "doi": "10.3390/ph15081009",
        "info_es": "Síntesis de 1,4-dihidropiridinas (1,4-DHP). Base estructural de los bloqueadores de canales de calcio.",
        "info_en": "Synthesis of 1,4-dihydropyridines (1,4-DHP). Structural basis for calcium channel blockers."
    },
    "Ugi (4-CR)": {
        "componentes": ["Aldehídos/Cetonas", "Aminas Primarias", "Ácidos Carboxílicos", "Isocianuros"],
        "smarts": '[C:1]=[O:2].[N:3]([H])([H]).[O:4]=[C:5][OH:6].[C-:7]#[N+:8][C:9]>>[C:1]([N:3][C:5]=[O:4])([C:7](=[O:2])[NH:8][C:9])',
        "producto_ejemplo": "CC(=O)NC(c1ccccc1)C(=O)NCc2ccccc2",
        "doi": "10.3762/bjoc.20.261",
        "info_es": "La 'reacción maestra' de las MCR. Genera bis-amidas (peptoides) en un solo paso.",
        "info_en": "The 'master reaction' of MCRs. Generates bis-amides (peptoids) in one step."
    },
    "Ugi-Smiles (4-CR)": {
        "componentes": ["Aldehídos", "Aminas Primarias", "Isocianuros", "Fenoles"],
        "smarts": '[C:1]=[O:2].[N:3]([H])([H]).[C-:4]#[N+:5][C:6].[c:7][OH:8]>>[C:1]([N:3][c:7])([C:4](=[O:2])[NH:5][C:6])',
        "producto_ejemplo": "CC(=O)NC(c1cc(O)ccc1)C(=O)NCc2ccccc2",
        "doi": "10.1016/B978-0-12-817467-8.00002-5",
        "info_es": "Variante del Ugi que involucra reordenamiento de Smiles.",
        "info_en": "Ugi variant involving Smiles rearrangement."
    },
    "Asinger (4-CR)": {
        "componentes": ["Alfa-Halo Carbonilos", "Amoniaco/Aminas", "Carbonilos"],
        "smarts": '[Cl,Br,I:1][CH1,CH2:2][C:3]=[O:4].[NH3:5].[S:6].[C:7]=[O:8]>>[C:2]1[C:3]=[N:5][C:7]([*:8])[S:6]1',
        "opciones_centrales": {"NaSH": "[S-]"},
        "producto_ejemplo": "Cc1c(C=O)ncs1",
        "doi": "10.1016/B978-0-12-817467-8.00002-5",
        "info_es": "Síntesis de 3-tiazolinas y 3-tiazoles. Precursores de penicilinas.",
        "info_en": "Synthesis of 3-thiazolines and 3-thiazoles. Precursors to penicillins."
    },
    "Bucherer-Bergs (4-CR)": {
        "componentes": ["Cetonas"],
        "smarts": '[C:1](=[O:2])([C:3])([C:4]).[C-:5]#[N:6].[NH3:7].[C:8](=[O:9])=[O:10]>>[C:1]1([C:3])([C:4])[NH:6][C:8](=[O:9])[NH:7][C:5]1=[O:2]',
        "opciones_centrales": {"Cianuro (KCN)": "[C-]#[N]", "Carbonato de Amonio": "NC(=O)N", "CO2": "O=C=O"},
        "producto_ejemplo": "CC1(C)NC(=O)NC1=O",
        "doi": "10.1016/B978-0-12-817467-8.00002-5",
        "info_es": "Síntesis de hidantoínas (imidazolidina-2,4-diona).",
        "info_en": "Synthesis of hydantoins (imidazolidine-2,4-dione)."
    }
}

# ════════════════════════════════════════════════════════════════════════
# v1.1.0 (Core) reaction set
# ════════════════════════════════════════════════════════════════════════
# For the v1.1.0 release we ship three 3‑component MCRs only (per academic scope).
# Ugi (4‑CR) and other reactions remain in the source tree for future packs/plugins.
V1_ENABLED_REACTIONS = [
    "Biginelli (3-CR)",
    "GBB (3-CR)",
    "Gewald (3-CR)",
]

# Filter catalogue to the v1.1.0 core set. Prefer the modular catalogue so all
# entrypoints share a single active reaction definition.
_catalog_source = _MCR_CATALOGO_MOD if isinstance(_MCR_CATALOGO_MOD, dict) else MCR_CATALOGO
MCR_CATALOGO = {k: _catalog_source[k] for k in V1_ENABLED_REACTIONS if k in _catalog_source}

# ════════════════════════════════════════════════════════════════════════
# DATA HELPERS
# ════════════════════════════════════════════════════════════════════════
def cargar_dataframe(filepath):
    if _cargar_dataframe_mod is None:
        raise ImportError("mcrg.loaders not available")
    return _cargar_dataframe_mod(filepath, pd=pd)


def cargar_dataframe_with_report(filepath, validate_rdkit: bool = True):
    if _cargar_dataframe_with_report_mod is None:
        raise ImportError("mcrg.loaders not available")
    return _cargar_dataframe_with_report_mod(
        filepath,
        pd=pd,
        validate_rdkit=bool(validate_rdkit),
        Chem=Chem,
        _CHEM_READY=bool(_CHEM_READY),
    )

def run_mcr(
    mcr_key,
    file_paths,
    core_smiles_list=None,
    threshold=50.0,
    progress_cb=None,
    standardize=True,
    ideal_rule="Lipinski",
):
    if _run_mcr_mod is None:
        raise ImportError("mcrg.engine not available")
    return _run_mcr_mod(
        mcr_key,
        file_paths,
        MCR_CATALOGO,
        core_smiles_list=core_smiles_list,
        threshold=threshold,
        progress_cb=progress_cb,
        standardize=standardize,
        ideal_rule=ideal_rule,
        pd=pd,
        Chem=Chem,
        AllChem=AllChem,
        Descriptors=Descriptors,
        Lipinski=Lipinski,
        _CHEM_READY=bool(_CHEM_READY),
    )

def mol_to_photoimage(smiles, size=(300, 250)):
    """
    Return (photoimage, error_message). Never raises.
    Some SMILES may parse but still fail drawing/sanitization.
    """
    if not _CHEM_READY or Image is None or ImageTk is None:
        return None, "RDKit/Pillow still loading"
    try:
        s = (smiles or "").strip()
        if not s:
            return None, "Empty SMILES"

        if _parse_smiles_flexible_mod is not None:
            mol = _parse_smiles_flexible_mod(s, Chem)
        else:
            mol = Chem.MolFromSmiles(s)
            if mol is None:
                # try a more permissive load then sanitize
                mol = Chem.MolFromSmiles(s, sanitize=False)
                if mol is None:
                    return None, "Invalid SMILES"
                try:
                    Chem.SanitizeMol(mol)
                except Exception as e:
                    return None, f"Sanitize failed: {str(e)[:120]}"
        if mol is None:
            return None, "Invalid SMILES"

        img = Draw.MolToImage(mol, size=size)
        return ImageTk.PhotoImage(img), ""
    except Exception as e:
        return None, f"Draw failed: {str(e)[:140]}"

# ════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ════════════════════════════════════════════════════════════════════════
class MCRGApp:
    # v1.1.0 core: no Chemical Space tab (future pack)
    TAB_IDS = ["motor", "resultados", "admet", "guide", "acerca"]
    def __init__(self):
        if not _TK_READY:
            raise RuntimeError(
                "Tkinter is not available in this Python environment. "
                "Install Tk support or use the packaged Moleku application."
            )
        self.root = ctk.CTk() if HAS_CTK else tk.Tk()
        self.root.title("Moleku v1.1.0"); self.root.geometry("950x700"); self.root.minsize(800, 600)
        self.root.configure(bg=CL["bg"])
        
        self.lang_var = StringVar(value="English")
        self.mcr_var = StringVar(value="Biginelli (3-CR)")
        self.threshold_var = DoubleVar(value=0.0)
        self.standardize_var = BooleanVar(value=True)
        self.ideal_rule_var = StringVar(value="Lipinski")
        self.filter_var = StringVar(value="Ideal")
        self.admet_search_var = StringVar(value="")
        self._custom_table_cols = None
        self.plot_var = StringVar(value="Score Distribution")
        self.versus_var = StringVar(value="Off")
        self.df_admet_all = None
        self.df_admet_view = None
        self._admet_mol_img_ref = None

        # Feature gates for v1.1.0 core (keep heavy/optional exports as future packs)
        self.features = {
            "export_pdf": True,
            "custom_zip": False,
            # ADMET-IA: keep both the web shortcut and the local prediction button.
            # Local prediction requires the optional 'admet-ai' package (handled at runtime).
            "admet_local": True,
            "export_zip_3d": True,
        }
        self.feedback_url = "https://mlkfeed.framer.website"
        
        self.file_paths = {}; self.file_svars = {}
        self.df_all = None; self.df_ideal = None
        self.central_vars = {}; self._mol_img_ref = None
        self._preview_img_refs = []; self._file_slot_widgets = []
        self._preview_resize_job = None
        self._plot_canvases = []; self._plot_cache = {}
        self._updating_plots = False; self._last_plot_config = None
        self.total_generated = 0; self.total_discarded = 0
        self._runtime_monitor_after = None
        self._runtime_monitor_state = None
        
        threading.Thread(target=_load_heavy, daemon=True).start()
        self._build_ui()
        self._start_runtime_monitor()

    def run(self):
        self.root.mainloop()

    def t(self, key, **kw):
        lang = self.lang_var.get()
        locales = LOCALES.get(lang, LOCALES["English"])
        s = locales.get(key, LOCALES["English"].get(key, key))
        return s.format(**kw) if kw else s

    def _col_label(self, col: str) -> str:
        if _col_label_mod is None:
            raise ImportError("mcrg.ui_common not available")
        return _col_label_mod(self, globals(), col)

    def _refresh_table_headings(self):
        if _refresh_table_headings_mod is None:
            raise ImportError("mcrg.ui_table_headings not available")
        return _refresh_table_headings_mod(self, globals())

    def _get_font(self, base_size, bold=False):
        if _get_font_mod is None:
            raise ImportError("mcrg.ui_common not available")
        return _get_font_mod(self, globals(), base_size, bold)
    def _btn(self, p, **kw):
        if _btn_mod is None:
            raise ImportError("mcrg.ui_common not available")
        return _btn_mod(self, globals(), p, **kw)
    def _lbl(self, p, **kw):
        if _lbl_mod is None:
            raise ImportError("mcrg.ui_common not available")
        return _lbl_mod(self, globals(), p, **kw)
    def _frame(self, p, **kw):
        if _frame_mod is None:
            raise ImportError("mcrg.ui_common not available")
        return _frame_mod(self, globals(), p, **kw)

    def _build_ui(self):
        if _build_ui_mod is None:
            raise ImportError(f"mcrg.ui_common not available (import_error={_ui_common_import_error})")
        return _build_ui_mod(self, globals())

    def _build_motor(self):
        if _build_motor_mod is None:
            raise ImportError("mcrg.ui_motor not available")
        return _build_motor_mod(self, globals())

    def _build_resultados(self):
        if _build_results_mod is None:
            raise ImportError("mcrg.ui_results not available")
        return _build_results_mod(self, globals())

    def _build_admet(self):
        if _build_admet_mod is None:
            raise ImportError("mcrg.ui_admet_tab not available")
        return _build_admet_mod(self, globals())

    def _update_results_counter(self):
        if _update_results_counter_mod is None:
            raise ImportError("mcrg.ui_results_helpers not available")
        return _update_results_counter_mod(self, globals())

    def _refresh_results_help_panels(self):
        if _refresh_results_help_panels_mod is None:
            raise ImportError("mcrg.ui_results_helpers not available")
        return _refresh_results_help_panels_mod(self, globals())

    def _apply_results_info_layout(self):
        if _apply_results_info_layout_mod is None:
            raise ImportError("mcrg.ui_results_helpers not available")
        return _apply_results_info_layout_mod(self, globals())

    def _toggle_results_info_panels(self):
        if _toggle_results_info_panels_mod is None:
            raise ImportError("mcrg.ui_results_helpers not available")
        return _toggle_results_info_panels_mod(self, globals())

    def _build_espacio(self):
        if _build_space_mod is None:
            raise ImportError("mcrg.ui_space not available")
        return _build_space_mod(self, globals())

    def _build_guide(self):
        if _build_guide_mod is None:
            raise ImportError("mcrg.ui_guide not available")
        return _build_guide_mod(self, globals())

    def _build_acerca(self):
        if _build_about_mod is None:
            raise ImportError("mcrg.ui_about not available")
        return _build_about_mod(self, globals())

    def _make_hyperlink(self, parent, text, url, font_size=11):
        if _make_hyperlink_mod is None:
            raise ImportError("mcrg.ui_nav_i18n not available")
        return _make_hyperlink_mod(self, globals(), parent, text, url, font_size)

    def _show_plot_settings(self):
        if _show_plot_settings_mod is None:
            raise ImportError("mcrg.ui_dialogs not available")
        return _show_plot_settings_mod(self, globals())

    def _download_example(self, fmt):
        if _download_example_mod is None:
            raise ImportError("mcrg.ui_app_actions not available")
        return _download_example_mod(self, globals(), fmt)

    def _download_example_pack(self, pack_key):
        if _download_example_pack_mod is None:
            raise ImportError("mcrg.ui_app_actions not available")
        return _download_example_pack_mod(self, globals(), pack_key)

    def _open_feedback(self):
        if _open_feedback_mod is None:
            raise ImportError("mcrg.ui_app_actions not available")
        return _open_feedback_mod(self, globals())

    def _update_preview(self):
        if _update_preview_mod is None:
            raise ImportError("mcrg.ui_preview not available")
        return _update_preview_mod(self, globals())

    def _schedule_preview_redraw(self):
        if _schedule_preview_redraw_mod is None:
            raise ImportError("mcrg.ui_preview not available")
        return _schedule_preview_redraw_mod(self, globals())

    def _run(self):
        if _run_clicked_mod is None:
            raise ImportError("mcrg.ui_run not available")
        return _run_clicked_mod(self, globals())

    def _clear_results(self):
        if _clear_results_mod is None:
            raise ImportError("mcrg.ui_results_helpers not available")
        return _clear_results_mod(self, globals())

    def _restart_app(self):
        if _restart_app_mod is None:
            raise ImportError("mcrg.ui_app_actions not available")
        return _restart_app_mod(self, globals())

    def _apply_filter(self):
        if _apply_filter_mod is None:
            raise ImportError("mcrg.ui_table not available")
        return _apply_filter_mod(self, globals())

    def _apply_admet_filter(self):
        if _apply_admet_filter_mod is None:
            raise ImportError("mcrg.ui_admet_tab not available")
        return _apply_admet_filter_mod(self, globals())

    def _show_table_columns_dialog(self):
        if _show_table_columns_dialog_mod is None:
            raise ImportError("mcrg.ui_dialogs not available")
        return _show_table_columns_dialog_mod(self, globals())

    def _sort(self, col):
        if _sort_tree_mod is None:
            raise ImportError("mcrg.ui_table not available")
        return _sort_tree_mod(self, globals(), col)

    def _sort_admet(self, col):
        if _sort_admet_tree_mod is None:
            raise ImportError("mcrg.ui_admet_tab not available")
        return _sort_admet_tree_mod(self, globals(), col)

    def _on_tree_select(self, event):
        if _on_tree_select_mod is None:
            raise ImportError("mcrg.ui_table not available")
        return _on_tree_select_mod(self, globals(), event)

    def _on_admet_select(self, event):
        if _on_admet_select_mod is None:
            raise ImportError("mcrg.ui_admet_tab not available")
        return _on_admet_select_mod(self, globals(), event)

    def _exp_csv(self):
        if _exp_csv_mod is None:
            raise ImportError("mcrg.ui_exports_simple not available")
        return _exp_csv_mod(self, globals())

    def _exp_xlsx(self):
        if _exp_xlsx_mod is None:
            raise ImportError("mcrg.ui_exports_simple not available")
        return _exp_xlsx_mod(self, globals())

    def _exp_pdf(self):
        if _exp_pdf_mod is None:
            raise ImportError("mcrg.ui_exports_simple not available")
        return _exp_pdf_mod(self, globals())

    def _exp_table(self):
        if _exp_table_mod is None:
            raise ImportError("mcrg.ui_exports_simple not available")
        return _exp_table_mod(self, globals())

    def _export_pdf(self, df, fp):
        if _export_pdf_mod is None:
            raise ImportError("mcrg.export_pdf not available")
        return _export_pdf_mod(self, globals(), df, fp)
    def _export_file(self, ext, save_fn):
        if _export_file_mod is None:
            raise ImportError("mcrg.ui_exports_simple not available")
        return _export_file_mod(self, globals(), ext, save_fn)

    def _exp_zip(self):
        if _exp_zip_3d_mod is None:
            raise ImportError("mcrg.ui_export_3d not available")
        return _exp_zip_3d_mod(self, globals())

    def _exp_bundle(self):
        if _exp_bundle_mod is None:
            raise ImportError("mcrg.ui_exports_heavy not available")
        return _exp_bundle_mod(self, globals())

    def _exp_paper(self):
        if _exp_paper_mod is None:
            raise ImportError("mcrg.ui_exports_heavy not available")
        return _exp_paper_mod(self, globals())

    def _show_custom_zip_dialog(self):
        if _show_custom_zip_dialog_mod is None:
            raise ImportError("mcrg.ui_dialogs not available")
        return _show_custom_zip_dialog_mod(self, globals())

    def _export_paper_dataset_zip(self, zip_path: str, export_options: dict | None = None, *, manifest_basename: str | None = None) -> dict:
        if _export_paper_dataset_zip_wiring_mod is None:
            raise ImportError("mcrg.ui_export_wiring not available")
        return _export_paper_dataset_zip_wiring_mod(self, globals(), zip_path, export_options, manifest_basename=manifest_basename)

    def _export_research_bundle_zip(self, zip_path: str) -> dict:
        if _export_research_bundle_zip_wiring_mod is None:
            raise ImportError("mcrg.ui_export_wiring not available")
        return _export_research_bundle_zip_wiring_mod(self, globals(), zip_path)

    # ──────────────────────────────────────────────────────────────────
    # ADMET-IA helpers (clipboard + optional local ADMET-AI predictions)
    # ──────────────────────────────────────────────────────────────────
    def _get_selected_smiles(self):
        if _get_selected_smiles_mod is None:
            raise ImportError("mcrg.ui_clipboard_helpers not available")
        return _get_selected_smiles_mod(self, globals())

    def _get_ideal_smiles(self):
        if _get_ideal_smiles_mod is None:
            raise ImportError("mcrg.ui_clipboard_helpers not available")
        return _get_ideal_smiles_mod(self, globals())

    def _copy_to_clipboard(self, text: str):
        if _copy_to_clipboard_mod is None:
            raise ImportError("mcrg.ui_clipboard_helpers not available")
        return _copy_to_clipboard_mod(self, globals(), text)

    def _start_runtime_monitor(self):
        def tick():
            try:
                if _dependency_status_mod is not None:
                    dep_txt = _dependency_status_mod(chem_ready=bool(_CHEM_READY), pd_obj=pd, image_obj=Image)
                else:
                    dep_txt = "Runtime status unavailable"
                if _sample_usage_mod is not None:
                    perf_txt, self._runtime_monitor_state = _sample_usage_mod(self._runtime_monitor_state)
                else:
                    perf_txt = "CPU: n/a | RAM: n/a | GPU: n/a"
                for name, txt in (("lbl_runtime_status", dep_txt), ("lbl_admet_runtime_status", dep_txt)):
                    w = getattr(self, name, None)
                    if w and hasattr(w, "configure"):
                        (w.configure(text=txt) if HAS_CTK else w.config(text=txt))
                for name, txt in (("lbl_perf_status", perf_txt), ("lbl_admet_perf_status", perf_txt)):
                    w = getattr(self, name, None)
                    if w and hasattr(w, "configure"):
                        (w.configure(text=txt) if HAS_CTK else w.config(text=txt))
            except Exception:
                pass
            try:
                self._runtime_monitor_after = self.root.after(1000, tick)
            except Exception:
                self._runtime_monitor_after = None

        tick()

    def _admet_copy_selected_smiles(self):
        if _admet_copy_selected_smiles_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _admet_copy_selected_smiles_mod(self, globals())

    def _admet_copy_ideal_smiles(self):
        if _admet_copy_ideal_smiles_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _admet_copy_ideal_smiles_mod(self, globals())

    def _admet_open_web(self):
        if _admet_open_web_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _admet_open_web_mod(self, globals())

    def _admet_predict_selected_local(self):
        if _admet_predict_selected_local_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _admet_predict_selected_local_mod(self, globals())

    def _admet_predict_visible_local(self):
        if _admet_predict_visible_local_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _admet_predict_visible_local_mod(self, globals())

    def _admet_predict_ideal_local(self):
        if _admet_predict_ideal_local_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _admet_predict_ideal_local_mod(self, globals())

    def _admet_predict_results_local(self):
        if _admet_predict_results_local_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _admet_predict_results_local_mod(self, globals())

    def _admet_predict_pasted_local(self, smiles_text: str):
        if _admet_predict_pasted_local_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _admet_predict_pasted_local_mod(self, globals(), smiles_text)

    def _show_admet_predictions(self, preds_df, source_df=None, source_smiles=None):
        if _show_admet_predictions_mod is None:
            raise ImportError("mcrg.ui_admet not available")
        return _show_admet_predictions_mod(self, globals(), preds_df, source_df=source_df, source_smiles=source_smiles)

    def _refresh_admet_labels(self):
        if _refresh_admet_labels_mod is None:
            raise ImportError("mcrg.ui_admet_tab not available")
        return _refresh_admet_labels_mod(self, globals())

    def _clear_admet_view(self):
        if _clear_admet_view_mod is None:
            raise ImportError("mcrg.ui_admet_tab not available")
        return _clear_admet_view_mod(self, globals())

    def _export_admet_csv(self):
        if _export_admet_csv_mod is None:
            raise ImportError("mcrg.ui_admet_tab not available")
        return _export_admet_csv_mod(self, globals())

    def _render_espacio(self):
        if _render_espacio_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _render_espacio_mod(self, globals())

    def _draw_plots(self):
        if _draw_plots_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _draw_plots_mod(self, globals())

    def _prepare_plot_data(self, plot_key):
        if _prepare_plot_data_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _prepare_plot_data_mod(self, globals(), plot_key)

    def _draw_empty_state(self, cv, key):
        if _draw_empty_state_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _draw_empty_state_mod(self, globals(), cv, key)

    def _render_from_cache(self, cv, key, data):
        if _render_from_cache_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _render_from_cache_mod(self, globals(), cv, key, data)

    def _draw_single_plot(self, cv, key, data):
        if _draw_single_plot_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _draw_single_plot_mod(self, globals(), cv, key, data)
            
    def _get_xlabel(self, key):
        if _get_xlabel_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _get_xlabel_mod(self, key)

    def _get_ylabel(self, key):
        if _get_ylabel_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _get_ylabel_mod(self, key)

    def _draw_embedding_2d(self, cv, cw, ch, m, data):
        if _draw_embedding_2d_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _draw_embedding_2d_mod(self, globals(), cv, cw, ch, m, data)

    def _draw_plot_legend(self, cv, cw, ch, m, title, lines):
        if _draw_plot_legend_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _draw_plot_legend_mod(self, globals(), cv, cw, ch, m, title, lines)

    def _create_professional_plot_template(self, cv, cw, ch, m, title, xlabel, ylabel):
        if _create_professional_plot_template_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _create_professional_plot_template_mod(self, globals(), cv, cw, ch, m, title, xlabel, ylabel)

    def _draw_histogram(self, cv, cw, ch, m, data):
        if _draw_histogram_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _draw_histogram_mod(self, globals(), cv, cw, ch, m, data)

    def _draw_class_hist(self, cv, cw, ch, m, data):
        if _draw_class_hist_mod is None:
            raise ImportError("mcrg.plot_canvas not available")
        return _draw_class_hist_mod(self, globals(), cv, cw, ch, m, data)

    def _export_plots_dialog(self):
        if not self._plot_canvases: messagebox.showwarning("!", self.t("no_datos")); return
        folder = filedialog.askdirectory(title="Select folder to save plots")
        if not folder: return
        try:
            self._export_plots_paper_ready(folder)
            messagebox.showinfo("✅ Success", f"Paper-ready plots exported to {folder}")
        except Exception as e: messagebox.showerror("Error", str(e))

    def _export_plots_paper_ready(self, folder: str):
        if _export_plots_paper_ready_mod is None:
            raise ImportError("mcrg.plots not available")

        return _export_plots_paper_ready_mod(
            folder,
            plot_canvases=getattr(self, "_plot_canvases", []),
            prepare_plot_data=self._prepare_plot_data,
            get_xlabel=self._get_xlabel,
            t=self.t,
            filter_value=self.filter_var.get() if hasattr(self, "filter_var") else "",
            lang_value=self.lang_var.get() if hasattr(self, "lang_var") else "",
            plot_settings=dict(PLOT_SETTINGS),
            Chem=Chem,
        )

    def _refresh_slots(self):
        if _refresh_slots_mod is None:
            raise ImportError("mcrg.ui_motor_slots not available")
        return _refresh_slots_mod(self, globals())

    def _clear_motor_inputs(self):
        if _clear_motor_inputs_mod is None:
            raise ImportError("mcrg.ui_motor_slots not available")
        return _clear_motor_inputs_mod(self, globals())

    def _browse_file(self, component):
        if _browse_file_mod is None:
            raise ImportError("mcrg.ui_motor_slots not available")
        return _browse_file_mod(self, globals(), component)

    def _switch_tab(self, tid):
        if _switch_tab_mod is None:
            raise ImportError("mcrg.ui_nav_i18n not available")
        return _switch_tab_mod(self, globals(), tid)

    def _on_lang_change(self):
        if _on_lang_change_mod is None:
            raise ImportError("mcrg.ui_nav_i18n not available")
        return _on_lang_change_mod(self, globals())

    def _update_labels(self):
        if _update_labels_mod is None:
            raise ImportError("mcrg.ui_nav_i18n not available")
        return _update_labels_mod(self, globals())

def main():
    """Entry point for both direct execution and PyInstaller builds."""
    MCRGApp().run()


if __name__ == "__main__":
    try:
        _argv_text = " ".join(sys.argv)
        _is_mp_child = (
            "--multiprocessing-fork" in sys.argv
            or "multiprocessing.spawn" in _argv_text
            or "multiprocessing.resource_tracker" in _argv_text
            or "spawn_main" in _argv_text
        )
        if _is_mp_child:
            import multiprocessing as _mp
            _mp.freeze_support()
    except Exception:
        pass
    main()
