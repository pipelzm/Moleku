from __future__ import annotations

"""
i18n / UI text resources for Moleku.

Kept in a dedicated module so the GUI entrypoint (`mcrg_desktop.py`) stays smaller and
logic can be unit-tested without dragging the full UI.
"""

# Component label translations for the MOTOR tab (display-only; internal keys remain Spanish)
COMPONENT_LABELS_EN = {
    "Aldehídos": "Aldehydes",
    "Aldehídos/Cetonas": "Aldehydes/Ketones",
    "Cetonas": "Ketones",
    "Carbonilos": "Carbonyls",
    "Carbonilos Enolizables": "Enolizable Carbonyls",
    "Beta-Cetoésteres": "β-Ketoesters",
    "Beta-Cetoéster (Equiv 1)": "β-Ketoester (Equiv 1)",
    "Beta-Cetoéster (Equiv 2)": "β-Ketoester (Equiv 2)",
    "Ácidos Carboxílicos": "Carboxylic Acids",
    "Ácidos Borónicos": "Boronic Acids",
    "Isocianuros": "Isocyanides",
    "Aminas": "Amines",
    "Aminas Primarias": "Primary Amines",
    "Aminas Sec/Prim": "Secondary/Primary Amines",
    "Fenoles": "Phenols",
    "Fosfitos Dialquílicos": "Dialkyl Phosphites",
    "2-Aminoazinas": "2-Aminoazines",
    "Anilinas": "Anilines",
    "Alfa-Cianoésteres": "α-Cyanoesters",
    "Alfa-Halo Carbonilos": "α-Halo Carbonyls",
    "Amoniaco/Aminas": "Ammonia/Amines",
}


def display_component_name(comp: str, lang: str) -> str:
    # The reaction catalogue keeps component keys in Spanish for stability.
    # UI rule: only Spanish shows Spanish component labels; all other UI languages
    # (English/German/Japanese/Chinese/…) use the English display mapping.
    return comp if lang == "Español" else COMPONENT_LABELS_EN.get(comp, comp)


# Core reagent label translations (display-only; internal keys remain as defined in MCR_CATALOGO)
CORE_REAGENT_LABELS_EN = {
    # Biginelli
    "Urea": "Urea",
    "Tiourea": "Thiourea",
    "Guanidina": "Guanidine",
    # Strecker / Bucherer-Bergs / others
    "Cianuro (HCN/KCN)": "Cyanide (HCN/KCN)",
    "Cianuro (KCN)": "Cyanide (KCN)",
    "Carbonato de Amonio": "Ammonium carbonate",
    "CO2": "CO₂",
    # Gewald / Asinger
    "Azufre (S8)": "Sulfur (S₈)",
    "NaSH": "NaSH",
    # Doebner
    "Ácido pirúvico": "Pyruvic acid",
}


def display_core_reagent_name(name: str, lang: str) -> str:
    return name if lang == "Español" else CORE_REAGENT_LABELS_EN.get(name, name)


PLOT_DESC = {
    "Score Distribution": {"es": "Distribución de Score: Histograma de compatibilidad química.", "en": "Score Distribution: Histogram of chemical compatibility."},
    "MW Distribution": {"es": "Distribución de Peso Molecular: Rango y frecuencia de MW.", "en": "MW Distribution: Molecular weight range and frequency."},
    "LogP Distribution": {"es": "Distribución de LogP: Rango y frecuencia de lipofilicidad.", "en": "LogP Distribution: Lipophilicity range and frequency."},
    "TPSA Distribution": {"es": "Distribución de TPSA: Área polar topológica.", "en": "TPSA Distribution: Topological polar area."},
    "HBA Distribution": {"es": "Distribución de HBA: Aceptores de puentes de hidrógeno.", "en": "HBA Distribution: Hydrogen bond acceptors."},
    "HBD Distribution": {"es": "Distribución de HBD: Donadores de puentes de hidrógeno.", "en": "HBD Distribution: Hydrogen bond donors."},
    "2D PCA (Descriptors)": {"es": "Mapa 2D (PCA) usando descriptores estándar (MW/LogP/TPSA/HBA/HBD).", "en": "2D map (PCA) using standard descriptors (MW/LogP/TPSA/HBA/HBD)."},
}


# NOTE: Keep keys stable; many UI elements use `t(key)` lookups.
LOCALES = {
    "Español": {
        "titulo": "Moleku v1.1.0", "tab_motor": "Motor {rxn}", "tab_resultados": "Resultados",
        "tab_espacio": "Espacio Químico", "tab_admet": "ADMET", "tab_acerca": "Sobre Nosotros", "tab_guide": "Guía",
        "feedback": "Feedback",
        "info_formato": "ℹ Formatos: .csv, .txt, .tsv, .xlsx, .xls, .ods, .json, .numbers  |  Columnas: NAME y SMILES",
        "csv_de": "Archivo de {comp}:", "examinar": "Examinar…", "reactivos_centrales": "Reactivos centrales:",
        "core_reagents_select_hint": "seleccione uno o varios",
        "core_reagents_selected": "Seleccionados",
        "core_reagents_selected_none": "ninguno",
        "core_reagents_tip": "Seleccione varios reactivos para generar TODAS las combinaciones en una ejecución.",
        "umbral": "Umbral score (%):", "iniciar": "▶  Iniciar generación virtual", "limpiar": "✕  Limpiar lista",
        "threshold_hint": "Descarta productos DESPUÉS de generarlos si su Compatibility_% queda por debajo del umbral, aunque cumplan alguna regla como Lipinski.",
        "standardize": "Estandarizar productos (desalado/neutralización)",
        "ideal_rule": "Criterio Ideal:",
        "ideal_rule_hint": "Clasifica los productos DESPUÉS de generarlos usando reglas de drug-likeness; no cambia la reacción ni los productos que el motor intenta formar.",
        "procesando": "Procesando…", "listo": "Listo.", "error_archivos": "Carga todos los archivos.",
        "registros": "registros", "productos": "productos", "ideales": "ideales",
        "exportar_csv": "Exportar CSV", "exportar_xlsx": "Exportar Sheets", "exportar_zip": "Exportar ZIP 3D",
        "exportar_bundle": "Exportar Research Bundle (ZIP)",
        "exportar_paper": "Exportar Paper Dataset (ZIP)",
        "exportar_custom_zip": "Custom ZIP",
        "custom_zip_title": "Exportar Custom ZIP",
        "custom_zip_hint": "Marca lo que deseas incluir en el ZIP. “Paper (completo)” equivale al export Paper Dataset.",
        "custom_zip_tables_all": "Tabla de resultados (CSV, todas las filas)",
        "custom_zip_tables_ideal": "Tabla de resultados (CSV, solo Ideal)",
        "custom_zip_descriptors": "Subconjunto descriptores (CSV)",
        "custom_zip_alerts": "Alertas MedChem (CSV)",
        "custom_zip_sdf": "Estructuras (SDF, propiedades embebidas)",
        "custom_zip_figures": "Figuras espacio químico (PNG/PDF/SVG + manifest)",
        "custom_zip_qc": "Informe QC (JSON + CSV motivos)",
        "custom_zip_schema": "Esquema de columnas (JSON)",
        "custom_zip_env": "Entorno (pip freeze + python + conda si existe)",
        "custom_zip_preset_paper": "Paper (completo)",
        "custom_zip_preset_tables": "Solo tablas",
        "custom_zip_preset_figures": "Solo figuras",
        "custom_zip_export": "Crear ZIP…",
        "custom_zip_cancel": "Cancelar",
        "custom_zip_need_option": "Selecciona al menos una opción de exportación.",
        "custom_zip_need_results": "Este ZIP requiere resultados cargados (tabla vacía).",
        "export_bundle_title": "Research Bundle",
        "export_bundle_msg": "Exportando bundle reproducible (CSV/SDF/plots/manifest).",
        "export_paper_title": "Paper Dataset",
        "export_paper_msg": "Exportando dataset estilo paper (tablas/figuras/schema/QC/entorno).",
        "export_3d_title": "Exportar ZIP 3D",
        "export_3d_msg": "Generando conformeros 3D. Puede tardar en datasets grandes.",
        "exportar_pdf": "Exportar PDF", "exportar_alta_calidad": "Exportar Alta Calidad", "no_datos": "Sin datos.",
        "export_table": "Exportar tabla",
        "export_table_title": "Exportar tabla de resultados",
        "export_table_hint": "Elige qué grupo de resultados y qué formato deseas exportar.",
        "export_scope": "Grupo de resultados",
        "export_format": "Formato",
        "export_format_csv": "CSV (.csv)",
        "export_format_xlsx": "Sheets (.xlsx)",
        "export_format_pdf": "PDF (.pdf)",
        "export_scope_empty": "Ese grupo no tiene filas para exportar.",
        "admet_copy_sel": "Copiar SMILES (selección)",
        "admet_copy_ideal": "Copiar SMILES (Ideal)",
        "admet_open_web": "Abrir ADMET-IA (web)",
        "admet_predict": "ADMET (local)",
        "admet_no_selection": "Selecciona una o más filas en la tabla.",
        "admet_clipboard_ok": "SMILES copiados al portapapeles.",
        "admet_missing_pkg": "Predicción local requiere el paquete 'admet-ai'.\n\nInstala:\n  pip install admet-ai",
        "admet_missing_pkg_app": "ADMET local no está disponible correctamente dentro de este ejecutable.\n\nUsa la compilación actualizada de Moleku o vuelve a generar la app incluyendo el runtime completo de ADMET.",
        "admet_results_title": "ADMET-IA — Predicciones",
        "admet_export_csv": "Exportar ADMET",
        "admet_export": "Exportar ADMET",
        "admet_export_title": "Exportar tabla ADMET",
        "admet_export_hint": "Elige qué candidatos ADMET analizados y qué formato deseas exportar.",
        "admet_tab_hint": "Pega uno o varios SMILES en esta pestaña o carga directamente candidatos generados desde Resultados para explorar sus predicciones ADMET locales como un buscador.",
        "admet_tab_input_title": "Entrada de candidatos",
        "admet_tab_input_hint": "Pega SMILES uno por línea, usa la barra para buscar candidatos ya calculados o importa candidatos Ideal/Warning generados por Moleku.",
        "admet_info_title": "Guía rápida ADMET",
        "admet_info_hint": "Paneles rápidos para entender cómo cargar candidatos, cómo interpretar las salidas y cómo exportar subconjuntos útiles desde ADMET.",
        "admet_tab_run_input": "Generar desde SMILES",
        "admet_tab_use_visible": "Usar resultados visibles",
        "admet_tab_use_ideal": "Usar resultados",
        "admet_tab_use_results": "Usar resultados",
        "admet_tab_search": "Buscar candidato/SMILES:",
        "admet_tab_search_clear": "Limpiar",
        "admet_tab_results_count": "Candidatos analizados: {n} / {total}",
        "admet_tab_no_predictions": "Aún no hay predicciones ADMET integradas.",
        "admet_tab_select_candidate": "Busca un candidato o genera predicciones para visualizar su estructura y sus salidas ADMET.",
        "admet_tab_candidate_title_empty": "Visor 2D",
        "admet_tab_candidate_title": "Visualizando: {candidate}",
        "admet_tab_candidate_smiles": "SMILES: {smiles}",
        "admet_tab_summary_title_empty": "Selected ADMET outputs",
        "admet_tab_summary_title": "Selected ADMET outputs — {candidate}",
        "admet_tab_summary_empty": "Las salidas ADMET del candidato seleccionado aparecerán aquí.",
        "admet_tab_no_input_smiles": "Pega al menos un SMILES válido en el cuadro de ADMET.",
        "admet_tab_no_results_visible": "No hay candidatos visibles en Resultados para enviar a ADMET.",
        "admet_tab_no_ideal_results": "No hay candidatos Ideal disponibles para enviar a ADMET.",
        "admet_tab_no_results_generated": "No hay candidatos Ideal/Warning generados con SMILES para enviar a ADMET.",
        "admet_tab_running": "Calculando ADMET local para {n} candidato(s)...",
        "admet_help_input_title": "Cómo cargar candidatos",
        "admet_help_input": (
            "• Puedes pegar SMILES directamente en el cuadro superior derecho, uno por línea.\n"
            "• También puedes importar automáticamente candidatos Ideal/Warning desde Resultados.\n"
            "• Se aceptan líneas con solo SMILES o pares nombre/SMILES separados por tabulador, coma o punto y coma.\n"
            "• Las líneas que empiezan con '#' se ignoran como comentarios y los SMILES repetidos se deduplican antes de ejecutar ADMET.\n"
            "• La barra de búsqueda filtra los candidatos ya calculados por nombre o por SMILES, sin volver a ejecutar ADMET."
        ),
        "admet_help_outputs_title": "Cómo leer ADMET Outputs",
        "admet_help_outputs": (
            "• El visor 2D muestra la estructura del candidato activo.\n"
            "• El panel 'Selected ADMET outputs' lista las salidas calculadas por ADMET local para ese candidato.\n"
            "• El visor y el panel se actualizan al buscar otro candidato, de modo que puedes comparar varios compuestos dentro de la misma pestaña.\n"
            "• Los valores presentados son predictivos y sirven para priorización temprana; no reemplazan validación experimental.\n"
            "• Señales de alerta frecuentes: permeabilidad muy baja, toxicidad alta o perfiles contradictorios entre candidatos aparentemente similares."
        ),
        "admet_help_workflow_title": "Workflow ADMET sugerido",
        "admet_help_workflow": (
            "1) Genera candidatos en Moleku o pega un lote externo de SMILES.\n"
            "2) Ejecuta ADMET local desde esta pestaña.\n"
            "3) Usa la barra superior para moverte rápidamente entre candidatos ya calculados.\n"
            "4) Revisa la estructura 2D y contrasta sus salidas ADMET para priorizar mejor/peor perfil.\n"
            "5) Exporta ADMET como CSV, Sheets o PDF; genera ZIP 3D desde la tabla de Resultados.\n"
            "6) Conserva los mejores candidatos para análisis más profundo o validación externa."
        ),
        "export_select_title_3d": "Seleccionar candidatos para ZIP 3D",
        "export_select_title_admet": "Seleccionar candidatos para exportar ADMET",
        "admet_select_title_results": "Seleccionar candidatos de Resultados para ADMET",
        "admet_select_hint_results": "Elige candidatos Ideal, candidatos Ideal + Warning con SMILES, o selecciona manualmente un subconjunto.",
        "admet_select_mode_ideal": "Usar todos los candidatos Ideal",
        "admet_select_mode_generated": "Usar candidatos Ideal + Warning (con SMILES)",
        "admet_select_mode_manual": "Seleccionar candidatos manualmente",
        "export_select_hint": "Elige si deseas exportar todos los candidatos Ideal, Ideal + Warning con SMILES, o seleccionar manualmente un subconjunto.",
        "export_select_mode_ideal": "Exportar todos los candidatos Ideal",
        "export_select_mode_generated": "Exportar Ideal + Warning (con SMILES)",
        "export_select_mode_manual": "Seleccionar manualmente algunos candidatos",
        "export_select_candidates": "Candidatos disponibles",
        "export_select_all": "Seleccionar todo",
        "export_select_clear": "Limpiar selección",
        "export_select_apply": "Exportar",
        "export_select_apply_use": "Usar candidatos",
        "export_select_cancel": "Cancelar",
        "export_select_need_candidates": "No hay candidatos disponibles para exportar.",
        "export_select_need_manual": "Selecciona al menos un candidato para exportar.",
        "filtro": "Filtro:", "ideal": "Ideal", "warning": "Warning", "error": "Error", "generated": "Generated", "todos": "Todos", "descartado": "Descartado",
        "table_view": "Vista tabla:",
        "table_view_custom": "Personalizada…",
        "table_cols_title": "Columnas visibles (tabla)",
        "table_cols_apply": "Aplicar",
        "table_cols_cancel": "Cancelar",
        "visor_2d": "Visor 2D", "grafico_titulo": "Espacio Químico", "grafico_sel": "Vista:",
        "stats_score": "Compatibilidad heurística (%)",
        "stats_mw": "Peso molecular (MW)",
        "stats_logp": "LogP",
        "stats_tpsa": "TPSA",
        "stats_hba": "HBA",
        "stats_hbd": "HBD",
        "stats_qed": "QED",
        "stats_fsp3": "Fracción sp3 (Fsp3)",
        "stats_rb": "Enlaces rotables (RB)",
        "stats_rings": "Anillos",
        "stats_heavy": "Átomos pesados",
        "stats_mr": "Refractividad molar (MR)",
        "stats_pains": "Alertas PAINS",
        "stats_brenk": "Alertas Brenk",
        "stats_has_stereo": "Estereoquímica",
        "stats_chiral_centers": "Centros quirales",
        "results_help_params_title": "¿Qué significan estos parámetros?",
        "results_help_params": (
            "• Compatibilidad heurística (%): puntaje 0–100 calculado desde LogP, MW y TPSA (mientras más alto, mejor según este modelo).\n"
            "• MW: peso molecular (Da).\n"
            "• LogP: lipofilicidad (aprox. método de RDKit).\n"
            "• TPSA: área polar topológica.\n"
            "• HBA/HBD: aceptores/donadores de H.\n"
            "• Enlaces rotables, átomos pesados, anillos, refractividad molar: descriptores estructurales adicionales (RDKit).\n"
            "• QED/Fsp3: métricas globales de 'drug-likeness' (heurísticas).\n"
            "• PAINS/Brenk: alertas estructurales (heurísticas; no sustituyen revisión medicinal).\n"
            "• InChIKey: identificador estándar; se usa para detectar duplicados.\n"
            "• Estereoquímica/Quiralidad:\n"
            "  - Has_Stereo: True si el SMILES del producto incluye estereo (centros quirales o E/Z).\n"
            "  - Chiral_Centers: número de centros quirales detectados por RDKit.\n"
            "  - Unassigned: centros quirales presentes pero sin R/S asignado (SMILES sin estereo definida).\n"
            "\n"
            "TABLA E IDIOMA\n"
            "- Los encabezados visibles se traducen según Español/English; los nombres de columna en CSV/export siguen siendo las claves internas (reproducibilidad).\n"
            "- 'Personalizada…' define columnas visibles incluso antes de tener datos (vista anticipada).\n"
            "\n"
            "CLASIFICACIÓN (Ideal / Warning / Error)\n"
            "- Ideal: depende del 'Criterio Ideal' seleccionado en el motor (Lipinski / Ghose / Veber / Egan / Muegge / Any / All).\n"
            "- Warning: existe producto con SMILES_Final, pero falla el criterio elegido o el umbral de score.\n"
            "- Error: no se pudo generar un producto/SMILES válido o falló la reacción/sanitización.\n"
            "- Duplicados: Is_Duplicate y Duplicate_Of respecto al primer InChIKey repetido.\n"
            "\n"
            "¿POR QUÉ SE USAN ESTOS PARÁMETROS?\n"
            "- MW/LogP/HBA/HBD/TPSA son descriptores estándar para estimar 'drug-likeness' y permeabilidad.\n"
            "- Los filtros (Lipinski/Ghose/Veber/Egan/Muegge) son heurísticos comunes para priorizar compuestos.\n"
            "\n"
            "SCORE / COMPATIBILIDAD (HEURÍSTICA) (%)\n"
            "- Se calcula con una penalización por desviarse de valores objetivo (LogP ~ 2.5, MW ~ 350, TPSA ~ 90).\n"
            "- Importante: NO es un modelo validado de actividad biológica/ADMET; úsalo como ranking heurístico interno.\n"
            "- El slider de 'Score threshold' descarta resultados por debajo del umbral (aparecen como Discarded con motivo 'Below threshold').\n"
            "\n"
            "EXPORTACIONES (resumen)\n"
            "- Bajo la tabla: Exportar tabla (CSV/Sheets/PDF), Exportar ZIP 3D, copiar SMILES y enviar candidatos a ADMET local.\n"
            "- Exportar tabla permite elegir Ideal / Warning / Error / Generated / Todos y el formato de salida.\n"
            "- ZIP 3D exporta candidatos generados con SMILES (Ideal y Warning) mediante su propio selector.\n"
            "- ADMET (local) ejecuta predicciones offline y alimenta la pestaña ADMET con búsqueda/visualización integrada.\n"
            "- En v1.1.0 (core), paquetes avanzados (Custom ZIP / bundles reproducibles / paper dataset / análisis extra) se liberan como plugins/packs.\n"
            "\n"
            "Failure_Reason\n"
            "- Explica el motivo exacto del descarte (p.ej. 'No products generated', 'Sanitize failed', 'Invalid reactant', 'Fails <Rule>', 'Below threshold')."
        ),
        "results_help_workflow_title": "Workflow de trabajo (resumen)",
        "results_help_workflow": (
            "1) Selecciona una reacción MCR y el 'Criterio Ideal' (motor).\n"
            "2) Carga un archivo por componente (NAME, SMILES) y opcionalmente selecciona reactivos centrales.\n"
            "3) El motor genera combinaciones (producto cartesiano) y ejecuta la reacción (SMARTS) con RDKit.\n"
            "4) (Opcional) Estandariza productos (desalado/neutralización).\n"
            "5) Cuando hay producto, calcula descriptores + compatibilidad (%) + reglas Pass_* + alertas MedChem.\n"
            "6) Calcula InChIKey y marca duplicados.\n"
            "7) Clasifica Ideal / Warning / Error según el criterio elegido y registra Failure_Reason.\n"
            "8) Resultados: filtra Ideal / Warning / Error / Generated / Todos; 'Personalizada…' para columnas; visor 2D al seleccionar fila.\n"
            "9) Exporta según necesidad: tabla CSV/XLSX/PDF o ZIP 3D.\n"
            "10) Para funciones avanzadas, usa los packs/plugins de próximas versiones."
        ),
        "results_help_views_title": "¿Cómo interpretar Ideal / Warning / Error?",
        "results_help_views": (
            "- Ideal: filas que cumplen el 'Criterio Ideal' activo en el motor (no solo Lipinski por defecto: puedes cambiar la regla).\n"
            "- Warning: estructuras generadas con SMILES_Final que no cumplen el criterio o umbral; revisarlas queda bajo responsabilidad del usuario.\n"
            "- Error: intentos fallidos sin producto válido generado.\n"
            "- Generated: todas las filas con SMILES_Final (Ideal + Warning).\n"
            "- Todos: todos los intentos evaluados, coherente con el contador Total de la corrida.\n"
            "\n"
            "EXPORTACIÓN POR FILTRO\n"
            "- Exportar tabla permite elegir grupo y formato explícitamente: CSV, Sheets (XLSX) o PDF.\n"
            "- ZIP 3D usa su propio selector de candidatos y puede incluir estructuras Warning generadas con SMILES."
        ),
        "results_toggle_info_hide": "Ocultar paneles de info",
        "results_toggle_info_show": "Mostrar paneles de info",
        "mcr_label": "MCR:", "data_preview": "Vista Previa de Datos", "limpiar_todo": "✕  Limpiar Todo",
        "reiniciar": "↻  Reiniciar", "resultados_limpiados": "Resultados limpiados",
        "sin_datos": "Sin datos cargados", "frecuencia": "Frecuencia", "desc_label": "Desc.",
        "producto": "Producto", "no_preview": "Sin vista previa para esta reacción",
        "restart_confirm": "¿Desea reiniciar toda la aplicación? Se perderán los datos no exportados.",
        "error_no_data": "No hay datos para exportar.", "export_plots_title": "Exportar Gráficos",
        "missing_libraries": "Bibliotecas faltantes",
        "no_valid_products": "No se generaron productos válidos. Verifica los archivos SMILES o baja el umbral.",
        "saved": "Guardado:",
        "guide_title": "Guía de Uso — Moleku",
        "guide_text": (
            "📘 BIENVENIDO A Moleku v1.1.0\n"
            "──────────────────────────────\n"
            "Moleku es una plataforma de escritorio profesional para Diseño de Fármacos Asistido por Computadora (CADD), que permite la generación rápida de librerías virtuales mediante Reacciones Multicomponente (MCR).\n\n"
            "> PASO 1: PREPARAR ARCHIVOS DE ENTRADA\n"
            "Cada archivo debe contener exactamente dos columnas: NAME (identificador) y SMILES (estructura molecular).\n"
            "✅ Formatos soportados: .csv, .txt, .tsv, .dat, .smi, .xlsx, .xls, .ods, .json, .numbers\n"
            "🔍 Separadores auto-detectados: coma, punto y coma, tabulación, espacio o pipe.\n"
            "🧪 Tipos de escritura SMILES aceptados: canónico, aromático en minúsculas, Kekule/no aromático, representaciones equivalentes con distinto orden atómico, formas isoméricas/estereoquímicas (`@`, `/`, `\\`) y CXSMILES compatible con RDKit.\n"
            "🗂 También se aceptan archivos de una sola columna SMILES y encabezados comunes como SMILES, Canonical_SMILES, Isomeric_SMILES o CXSMILES.\n"
            "📄 Estructura de ejemplo:\n"
            "    NAME,SMILES\n"
            "    Benzaldehído,c1ccccc1C=O\n"
            "    4-Nitrobenzaldehído,O=Cc1ccc([N+](=O)[O-])cc1\n"
            "    Cinamaldehído_E,O=C/C=C/c1ccccc1\n\n"
            "> PASO 2: SELECCIONAR REACCIÓN MCR\n"
            "En Moleku v1.1.0 (core) están disponibles solo tres MCR de 3 componentes: Biginelli (3-CR), GBB (3-CR) y Gewald (3-CR). Ugi (4-CR) y el resto de reacciones no forman parte de esta versión. El panel de Vista Previa muestra el esquema, DOI y notas mecanísticas.\n"
            "⚗️ Para reacciones con componentes centrales fijos, use los checkboxes. Seleccione uno o varios para generar AUTOMÁTICAMENTE todas las variaciones combinatorias en una sola ejecución.\n\n"
            "> PASO 3: CONFIGURAR Y EJECUTAR\n"
            "Cargue un archivo por cada componente externo. Ajuste el umbral de Score (0–100%). Presione '▶ Iniciar generación virtual'.\n"
            "⚙️ El motor calcula el producto cartesiano, mapea SMARTS con RDKit y evalúa cada producto con scoring + reglas de drug-likeness (Lipinski/Ghose/Veber/Egan/Muegge).\n"
            "🧼 Opcional: active 'Estandarizar productos' para desalado/neutralización y deduplicación por InChIKey.\n\n"
            "> PASO 4: ANALIZAR RESULTADOS\n"
            "Los resultados aparecen en 'Resultados'. Filtre por Ideal / Warning / Error / Generated / Todos. Haga clic en cualquier fila para ver la estructura 2D y propiedades.\n"
            "🧩 Use 'Personalizada…' para elegir qué columnas ver en la tabla (también sin datos, para preparar la vista).\n"
            "Los encabezados de la tabla respetan el idioma de la interfaz; los datos exportados mantienen nombres de columna estables.\n"
            "🧬 Quiralidad/estereoquímica: la tabla incluye Has_Stereo y el conteo de centros quirales (definidos/sin asignar) calculados desde SMILES_Final.\n"
            "💾 Bajo la tabla: Exportar tabla (CSV/Sheets/PDF), Exportar ZIP 3D, copiar SMILES y enviar candidatos generados a ADMET local.\n"
            "🧠 La pestaña ADMET funciona como un buscador integrado: puedes pegar SMILES, importar candidatos Ideal/Warning, navegar entre compuestos con la búsqueda y revisar sus salidas locales sin abrir popups.\n"
            "🧪 Los paneles plegables de ADMET resumen cómo cargar candidatos, cómo interpretar los resultados y qué workflow seguir para priorización.\n"
            "🧩 La exportación ADMET soporta CSV/Sheets/PDF. ZIP 3D está bajo la tabla de Resultados y puede incluir estructuras Warning generadas con SMILES.\n"
            "⚠️ Las predicciones ADMET son orientativas para cribado temprano; no sustituyen ensayos experimentales ni validación farmacológica.\n"
            "🧩 El resto de exportaciones avanzadas (Custom ZIP, bundles reproducibles, dataset tipo paper, etc.) se liberarán como packs/plugins en próximas versiones.\n"
            "💬 Usa el botón 'Feedback' (arriba a la derecha) para sugerir reacciones/features y reportar bugs.\n\n"
            "> PASO 5: EXPORTAR ZIP 3D\n"
            "Usa Exportar ZIP 3D bajo la tabla de Resultados para generar conformeros SDF de estructuras Ideal o Warning seleccionadas con SMILES.\n\n"
            "⚠️ SOLUCIÓN DE PROBLEMAS Y BUENAS PRÁCTICAS\n"
            "• 'Sin productos válidos': Reduzca el umbral o verifique la validez de los SMILES.\n"
            "• Errores RDKit: Ejecute `conda install -c conda-forge rdkit`.\n"
            "• Archivos .numbers de Apple: Expórtelos a .xlsx o .csv si fallan.\n"
            "• Mantenga archivos bajo 50,000 entradas por componente para rendimiento óptimo.\n\n"
            "- USE LOS BOTONES ABAJO PARA DESCARGAR PLANTILLAS GENÉRICAS O PACKS POR REACCIÓN -.\n"
        ),
        "guide_templates_title": "Descargar plantillas de ejemplo:",
        "guide_template_csv": "Plantilla CSV (.csv)",
        "guide_template_txt": "Plantilla TXT/TSV (.txt)",
        "guide_template_xlsx": "Plantilla Sheets (.xlsx)",
        "guide_packs_title": "Packs listos por reacción (.zip):",
        "guide_pack_biginelli": "Pack Biginelli",
        "guide_pack_gbb": "Pack GBB",
        "guide_pack_gewald": "Pack Gewald",
        "about_desc": "Es una plataforma de escritorio para CADD que permite generar librerías virtuales mediante MCR de 3 componentes (Biginelli, GBB y Gewald) y priorizar compuestos usando descriptores fisicoquímicos, reglas de drug-likeness (Lipinski/Ghose/Veber/Egan/Muegge), deduplicación por InChIKey y alertas MedChem (PAINS/Brenk). Exporta CSV/Sheets/PDF y un ZIP 3D (conformeros) para integrar con flujos académicos e industriales.",
        "about_footer": "Dependencias: RDKit | Pandas | Pillow | CustomTkinter\nLicencia: Apache License 2.0 • © 2026 Felipe Lizama Mora"
        ,
        # Web (Swiss-like) UI strings
        "web_title": "Moleku Web",
        "web_subtitle": "Plataforma Web",
        "web_nav_home": "Inicio",
        "web_nav_motor": "Motor",
        "web_nav_results": "Resultados",
        "web_nav_space": "Espacio",
        "web_nav_guide": "Guía",
        "web_nav_about": "Sobre",
        "web_welcome_title": "Bienvenido a Moleku",
        "web_welcome_subtitle": "Elige cómo quieres usar la plataforma: versión web o descargar la app de escritorio.",
        "web_welcome_open_web": "Abrir plataforma web",
        "web_welcome_download_desktop": "Descargar versión de escritorio (GitHub)",
        "web_welcome_hint": "Si buscas la app de escritorio, en GitHub encontrarás el código y (si está disponible) la sección de Releases/descargas.",
        "web_welcome_card_web_title": "Plataforma web",
        "web_welcome_card_web_desc": "Ejecuta el motor, explora resultados, visor 2D/3D, espacio químico y exportaciones desde el navegador.",
        "web_welcome_card_desktop_title": "App de escritorio",
        "web_welcome_card_desktop_desc": "Descarga el proyecto desde GitHub para usar la versión de escritorio y sus herramientas avanzadas.",
        "web_recommended": "Recomendado",
        "web_links_title": "Enlaces",
        "web_links_hint": "Accesos directos a perfiles e instituciones.",
        "web_inputs_title": "Entradas",
        "web_inputs_supported": "Soportados: csv/tsv/txt/xlsx/json/numbers/ods/smi.",
        "web_histogram": "histograma",
        "web_plot_not_available": "Gráfico no disponible para este run.",
        "web_viewer2d_title": "Visor 2D",
        "web_loading_2d": "Cargando visor 2D…",
        "web_download_3d_zip": "SDF 3D (ZIP)",
        "web_kind": "vista",
        "web_row": "Fila",
        "web_run": "Run",
        "web_status": "estado",
        "web_progress": "progreso",
        "web_all": "total",
        "web_run_log_qc": "Bitácora / QC",
        "web_run_setup_title": "Configuración de ejecución",
        "web_run_setup_subtitle": "Sube un archivo por componente y ejecuta el motor.",
        "web_reaction_label": "Reacción (MCR)",
        "web_threshold_label": "Umbral",
        "web_ideal_rule_label": "Regla Ideal",
        "web_standardize_label": "Estandarizar productos (desalado/neutralización)",
        "web_run_btn": "Run",
        "web_results_title": "Resultados",
        "web_results_empty_hint": "Ejecuta el motor para ver aquí un reporte estructurado (estado, QC, conteos, descargas).",
        "web_results_report_title": "Reporte de resultados",
        "web_run_id": "Run ID",
        "web_new_run": "Nuevo run",
        "web_download_zip": "Descargar ZIP",
        "web_loading": "Cargando…",
        "web_loading_table": "Cargando tabla…",
        "web_loading_space": "Cargando espacio químico…",
        "web_loading_3d": "Cargando visor 3D…",
        "web_pending_table": "Esperando tabla de resultados…",
        "web_pending_space": "Esperando espacio químico…",
        "web_pending_3d": "Esperando visor 3D…",
        "web_recent_runs": "Runs recientes",
        "web_recent_runs_hint": "Haz clic para reabrir un resultado previo.",
        "web_no_runs_yet": "Aún no hay runs.",
        "web_results_table": "Tabla de resultados",
        "web_view": "Vista",
        "web_section": "Sección",
        "web_rows": "Filas",
        "web_filter_ph": "Filtrar (SMILES/InChIKey…)",
        "web_apply": "Aplicar",
        "web_page": "página",
        "web_no_rows": "Sin filas.",
        "web_showing_rows": "Mostrando {n} filas.",
        "web_prev": "Anterior",
        "web_next": "Siguiente",
        "web_space_title": "Espacio químico",
        "web_space_desc": "PCA 2D sobre descriptores (MW/LogP/TPSA/HBA/HBD/RB/QED/Fsp3).",
        "web_download_pca_png": "Descargar PCA (PNG)",
        "web_download_pca_svg": "Descargar PCA (SVG)",
        "web_download_sdf": "Descargar SDF",
        "web_viewer3d_title": "Visor 3D",
        "web_viewer3d_desc": "Conformero ETKDG + MMFF renderizado con 3Dmol.js.",
        "web_molecule": "Molécula",
        "web_notes": "Notas",
        "web_viewer3d_notes": "Si una molécula falla el embedding 3D, prueba otra entrada.",
        "web_no_molecules_3d": "No hay moléculas disponibles para render 3D.",
        "web_conformer_unavailable": "Conformero 3D no disponible para esta entrada",
        "web_core_reagents": "Reactivos centrales",
        "web_core_reagents_hint": "Opcional (por defecto se usa la primera opción si no seleccionas ninguna).",
        "web_no_results_yet_title": "No hay resultados aún",
        "web_no_results_yet_hint": "Vuelve a Motor y ejecuta una reacción.",
        "web_lang_label": "Idioma"
        ,
        "web_guide_title": "Guía de Uso — Moleku Web",
        "web_guide_text": (
            "BIENVENIDO A Moleku WEB\n"
            "──────────────────────────────\n"
            "Moleku Web es la versión accesible desde navegador. Replica el flujo de la app de escritorio, pero la interfaz y navegación están adaptadas a web.\n\n"
            "PASO 1: PREPARAR ARCHIVOS DE ENTRADA\n"
            "Cada archivo debe contener dos columnas: NAME (identificador) y SMILES (estructura).\n"
            "Formatos comunes: CSV/TSV/TXT/XLSX. Si tienes .numbers, expórtalo a .csv o .xlsx.\n\n"
            "PASO 2: SELECCIONAR REACCIÓN (MCR)\n"
            "Elige la reacción y sube un archivo por componente.\n"
            "Si hay reactivos centrales, puedes seleccionar uno o varios para generar combinaciones.\n\n"
            "PASO 3: CONFIGURAR Y EJECUTAR\n"
            "Ajusta el umbral y la regla Ideal. Presiona Run y espera a que el estado llegue a 'done'.\n\n"
            "PASO 4: RESULTADOS / ESPACIO / 3D\n"
            "Explora la tabla por secciones, filtra, y exporta CSV/ZIP. En Espacio químico, descarga PCA (PNG/SVG). En 3D, selecciona moléculas para inspección.\n\n"
            "PLANTILLAS\n"
            "Usa los botones de descarga para obtener plantillas listas para completar."
        ),
        "web_about_desc": (
            "Moleku Web (Multi Component Reaction Generator) es la versión web de la plataforma para generar y analizar librerías virtuales basadas en MCRs "
            "para flujos de early drug discovery. Reutiliza el mismo núcleo computacional (RDKit + pandas) y expone resultados, visualización (PCA/3D) "
            "y exportaciones reproducibles desde el navegador."
        ),
        "web_link_linkedin": "LinkedIn",
        "web_link_github": "GitHub",
        "web_link_sbbcs": "SB&BCS Lab",
        "web_link_ufro": "UFRO",
        "web_templates_title": "Plantillas de ejemplo",
        "web_templates_hint": "Descarga plantillas (NAME,SMILES) para cada componente y completa tus bibliotecas.",
        "web_download_template_csv": "Descargar plantilla (CSV)",
        "web_download_template_smi": "Descargar plantilla (SMI)"
        ,
        "web_admet_title": "ADMET-IA",
        "web_admet_hint": "Copia SMILES y pégalos en ADMET-IA (web) para predicciones.",
        "web_copy_smiles_all": "Copiar SMILES (Todos)",
        "web_copy_smiles_ideal": "Copiar SMILES (Ideal)",
        "web_open_admet": "Abrir ADMET-IA (web)",
        "web_copied": "Copiado al portapapeles.",
        "web_plots_title": "Gráficos (distribuciones)",
        "web_plots_hint": "Histogramas rápidos para inspección (exportables en PNG).",
        "web_plot_score": "Score",
        "web_plot_mw": "MW",
        "web_plot_logp": "LogP",
        "web_plot_tpsa": "TPSA",
        "web_download_png": "Descargar PNG",
        "web_plot_settings": "Plot Settings",
        "web_ps_color_ideal": "Color (Ideal)",
        "web_ps_color_discard": "Color (Discarded)",
        "web_ps_plot_bg": "Fondo",
        "web_ps_axis_color": "Color ejes",
        "web_ps_grid_color": "Color grilla",
        "web_ps_font_size": "Tamaño fuente",
        "web_ps_font_bold": "Título en negrita",
        "web_ps_marker_size": "Tamaño marcador (PCA)",
        "web_ps_hist_bins": "Bins histograma",
        "web_ps_axis_width": "Grosor ejes",
        "web_ps_grid_width": "Grosor grilla",
        "web_ps_show_grid": "Mostrar grilla",
        "web_ps_show_legend": "Mostrar leyenda",
        "web_ps_legend_pos": "Posición leyenda",
        "web_ps_reset": "Restablecer",
        "web_ps_hint": "Sugerencia: usa colores hex (#RRGGBB). Se guarda en tu navegador."
    },
    "English": {
        "feedback": "Feedback",
        "titulo": "Moleku v1.1.0", "tab_motor": "Engine {rxn}", "tab_resultados": "Results",
        "tab_espacio": "Chemical Space", "tab_admet": "ADMET", "tab_acerca": "About", "tab_guide": "Guide",
        "info_formato": "ℹ Formats: .csv, .txt, .tsv, .xlsx, .xls, .ods, .json, .numbers  |  Columns: NAME and SMILES",
        "csv_de": "File for {comp}:", "examinar": "Browse…", "reactivos_centrales": "Core reagents:",
        "core_reagents_select_hint": "select one or multiple",
        "core_reagents_selected": "Selected",
        "core_reagents_selected_none": "none",
        "core_reagents_tip": "Select multiple reagents to generate ALL combinations in one run.",
        "umbral": "Score threshold (%):", "iniciar": "▶  Start virtual generation", "limpiar": "✕  Clear list",
        "threshold_hint": "Discards products AFTER generation if their Compatibility_% falls below the threshold, even if they satisfy a rule such as Lipinski.",
        "standardize": "Standardize products (desalt/neutralize)",
        "ideal_rule": "Ideal criterion:",
        "ideal_rule_hint": "Classifies products AFTER generation using drug-likeness rules; it does not change the reaction or which products the engine attempts to form.",
        "procesando": "Processing…", "listo": "Done.", "error_archivos": "Load all required files.",
        "registros": "records", "productos": "products", "ideales": "ideal",
        "exportar_csv": "Export CSV", "exportar_xlsx": "Export Sheets", "exportar_zip": "Export 3D ZIP",
        "exportar_bundle": "Export Research Bundle (ZIP)",
        "exportar_paper": "Export Paper Dataset (ZIP)",
        "exportar_custom_zip": "Custom ZIP",
        "custom_zip_title": "Custom ZIP export",
        "custom_zip_hint": "Choose what to include. “Paper (full)” matches the full Paper Dataset export.",
        "custom_zip_tables_all": "Results table (CSV, all rows)",
        "custom_zip_tables_ideal": "Results table (CSV, Ideal only)",
        "custom_zip_descriptors": "Descriptor subset (CSV)",
        "custom_zip_alerts": "MedChem alerts (CSV)",
        "custom_zip_sdf": "Structures (SDF with embedded properties)",
        "custom_zip_figures": "Chemical space figures (PNG/PDF/SVG + manifest)",
        "custom_zip_qc": "QC report (JSON + discard-reason CSV)",
        "custom_zip_schema": "Column schema (JSON)",
        "custom_zip_env": "Environment (pip freeze + python + conda if available)",
        "custom_zip_preset_paper": "Paper (full)",
        "custom_zip_preset_tables": "Tables only",
        "custom_zip_preset_figures": "Figures only",
        "custom_zip_export": "Create ZIP…",
        "custom_zip_cancel": "Cancel",
        "custom_zip_need_option": "Select at least one export option.",
        "custom_zip_need_results": "This export needs loaded results (table is empty).",
        "export_bundle_title": "Research Bundle",
        "export_bundle_msg": "Exporting reproducible bundle (CSV/SDF/plots/manifest).",
        "export_paper_title": "Paper Dataset",
        "export_paper_msg": "Exporting paper-grade dataset (tables/figures/schema/QC/environment).",
        "export_3d_title": "Export 3D ZIP",
        "export_3d_msg": "Generating 3D conformers. This can take a while for large datasets.",
        "exportar_pdf": "Export PDF", "exportar_alta_calidad": "Export High Quality", "no_datos": "No data.",
        "export_table": "Export Table",
        "export_table_title": "Export results table",
        "export_table_hint": "Choose which result scope and file format to export.",
        "export_scope": "Result scope",
        "export_format": "Format",
        "export_format_csv": "CSV (.csv)",
        "export_format_xlsx": "Sheets (.xlsx)",
        "export_format_pdf": "PDF (.pdf)",
        "export_scope_empty": "That scope has no rows to export.",
        "admet_copy_sel": "Copy SMILES (selection)",
        "admet_copy_ideal": "Copy SMILES (Ideal)",
        "admet_open_web": "Open ADMET-IA (web)",
        "admet_predict": "ADMET (local)",
        "admet_no_selection": "Select one or more rows in the table.",
        "admet_clipboard_ok": "SMILES copied to clipboard.",
        "admet_missing_pkg": "Local prediction requires the 'admet-ai' package.\n\nInstall:\n  pip install admet-ai",
        "admet_missing_pkg_app": "Local ADMET is not correctly available inside this executable.\n\nUse the updated Moleku build or rebuild the app with the full ADMET runtime included.",
        "admet_results_title": "ADMET-IA — Predictions",
        "admet_export_csv": "Export ADMET",
        "admet_export": "Export ADMET",
        "admet_export_title": "Export ADMET table",
        "admet_export_hint": "Choose which analyzed ADMET candidates and file format to export.",
        "admet_tab_hint": "Paste one or more SMILES in this tab or load generated candidates directly from Results to explore local ADMET predictions through a search-driven workflow.",
        "admet_tab_input_title": "Candidate input",
        "admet_tab_input_hint": "Paste one SMILES per line, use the search bar to revisit computed candidates, or import generated Ideal/Warning candidates from Moleku.",
        "admet_info_title": "ADMET quick guide",
        "admet_info_hint": "Short panels to explain candidate loading, output interpretation, and how to export useful subsets from ADMET.",
        "admet_tab_run_input": "Run pasted SMILES",
        "admet_tab_use_visible": "Use visible results",
        "admet_tab_use_ideal": "Use Results",
        "admet_tab_use_results": "Use Results",
        "admet_tab_search": "Search candidate/SMILES:",
        "admet_tab_search_clear": "Clear",
        "admet_tab_results_count": "Analyzed candidates: {n} / {total}",
        "admet_tab_no_predictions": "No integrated ADMET predictions yet.",
        "admet_tab_select_candidate": "Search for a candidate or generate predictions to visualize its structure and ADMET outputs.",
        "admet_tab_candidate_title_empty": "2D Viewer",
        "admet_tab_candidate_title": "Viewing: {candidate}",
        "admet_tab_candidate_smiles": "SMILES: {smiles}",
        "admet_tab_summary_title_empty": "Selected ADMET outputs",
        "admet_tab_summary_title": "Selected ADMET outputs — {candidate}",
        "admet_tab_summary_empty": "ADMET outputs for the selected candidate will appear here.",
        "admet_tab_no_input_smiles": "Paste at least one valid SMILES in the ADMET input box.",
        "admet_tab_no_results_visible": "There are no visible Results candidates to send to ADMET.",
        "admet_tab_no_ideal_results": "There are no Ideal candidates available to send to ADMET.",
        "admet_tab_no_results_generated": "There are no generated Ideal/Warning candidates with SMILES available to send to ADMET.",
        "admet_tab_running": "Running local ADMET for {n} candidate(s)...",
        "admet_help_input_title": "How to load candidates",
        "admet_help_input": (
            "• Paste SMILES directly into the upper-right input box, one per line.\n"
            "• You can also import generated Ideal/Warning candidates from Results.\n"
            "• Both plain SMILES lines and name/SMILES pairs separated by tabs, commas, or semicolons are accepted.\n"
            "• Lines starting with '#' are ignored as comments, and duplicate SMILES are removed before running ADMET.\n"
            "• The search bar filters candidates that were already computed, without re-running ADMET."
        ),
        "admet_help_outputs_title": "How to read ADMET Outputs",
        "admet_help_outputs": (
            "• The 2D viewer shows the active candidate structure.\n"
            "• 'Selected ADMET outputs' lists the local ADMET predictions for that candidate.\n"
            "• The viewer and output panel update as you search another candidate, so comparison stays inside the same tab.\n"
            "• These values are intended for early prioritization and do not replace experimental validation.\n"
            "• Common red flags include very poor permeability, high predicted toxicity, or contradictory profiles across similar candidates."
        ),
        "admet_help_workflow_title": "Suggested ADMET workflow",
        "admet_help_workflow": (
            "1) Generate candidates in Moleku or paste an external SMILES batch.\n"
            "2) Run local ADMET from this tab.\n"
            "3) Use the top search bar to move quickly across computed candidates.\n"
            "4) Review the 2D structure and compare ADMET outputs to rank the best/worst profiles.\n"
            "5) Export the ADMET table as CSV, Sheets, or PDF; generate 3D ZIP from the Results tab.\n"
            "6) Keep the strongest candidates for deeper analysis or external validation."
        ),
        "export_select_title_3d": "Select candidates for 3D ZIP export",
        "export_select_title_admet": "Select candidates for ADMET export",
        "admet_select_title_results": "Select Results candidates for ADMET",
        "admet_select_hint_results": "Choose Ideal candidates, Ideal + Warning candidates with SMILES, or manually select a subset.",
        "admet_select_mode_ideal": "Use all Ideal candidates",
        "admet_select_mode_generated": "Use Ideal + Warning candidates (with SMILES)",
        "admet_select_mode_manual": "Manually select candidates",
        "export_select_hint": "Choose whether to export all Ideal candidates, Ideal + Warning candidates with SMILES, or manually select a specific subset.",
        "export_select_mode_ideal": "Export all Ideal candidates",
        "export_select_mode_generated": "Export Ideal + Warning (with SMILES)",
        "export_select_mode_manual": "Manually select specific candidates",
        "export_select_candidates": "Available candidates",
        "export_select_all": "Select all",
        "export_select_clear": "Clear selection",
        "export_select_apply": "Export",
        "export_select_apply_use": "Use candidates",
        "export_select_cancel": "Cancel",
        "export_select_need_candidates": "There are no candidates available to export.",
        "export_select_need_manual": "Select at least one candidate to export.",
        "filtro": "Filter:", "ideal": "Ideal", "warning": "Warning", "error": "Error", "generated": "Generated", "todos": "All", "descartado": "Discarded",
        "table_view": "Table view:",
        "table_view_custom": "Custom…",
        "table_cols_title": "Visible columns (table)",
        "table_cols_apply": "Apply",
        "table_cols_cancel": "Cancel",
        "visor_2d": "2D Viewer", "grafico_titulo": "Chemical Space", "grafico_sel": "View:",
        "stats_score": "Heuristic compatibility (%)",
        "stats_mw": "Molecular Weight (MW)",
        "stats_logp": "LogP",
        "stats_tpsa": "TPSA",
        "stats_hba": "HBA",
        "stats_hbd": "HBD",
        "stats_qed": "QED",
        "stats_fsp3": "FractionCSP3 (Fsp3)",
        "stats_rb": "Rotatable bonds (RB)",
        "stats_rings": "Rings",
        "stats_heavy": "Heavy atoms",
        "stats_mr": "Molar refractivity (MR)",
        "stats_pains": "PAINS alerts",
        "stats_brenk": "Brenk alerts",
        "stats_has_stereo": "Stereochemistry",
        "stats_chiral_centers": "Chiral centers",
        "results_help_params_title": "What do these parameters mean?",
        "results_help_params": (
            "• Heuristic compatibility (%): 0–100 score computed from LogP, MW and TPSA (higher is better under this model).\n"
            "• MW: molecular weight (Da).\n"
            "• LogP: lipophilicity (RDKit estimate).\n"
            "• TPSA: topological polar surface area.\n"
            "• HBA/HBD: H-bond acceptors/donors.\n"
            "• Rotatable bonds, heavy atoms, ring count, molar refractivity: additional structural descriptors (RDKit).\n"
            "• QED/Fsp3: global drug-likeness heuristics.\n"
            "• PAINS/Brenk: structural alert heuristics (do not replace expert review).\n"
            "• InChIKey: standard identifier used for duplicate detection.\n"
            "• Stereochemistry/Chirality:\n"
            "  - Has_Stereo: True if the product SMILES encodes stereo (chiral centers or E/Z).\n"
            "  - Chiral_Centers: number of chiral centers detected by RDKit.\n"
            "  - Unassigned: chiral centers present but without R/S assignment (SMILES without defined stereo).\n"
            "\n"
            "TABLE HEADINGS & LANGUAGE\n"
            "- Visible column headers follow the UI language (English/Spanish); exported CSV keys stay stable for reproducibility.\n"
            "- 'Custom…' sets visible columns even before a run (preview layout).\n"
            "\n"
            "CLASSIFICATION (Ideal / Warning / Error)\n"
            "- Ideal: depends on the 'Ideal criterion' selected on the Engine tab (Lipinski / Ghose / Veber / Egan / Muegge / Any / All).\n"
            "- Warning: product exists and SMILES_Final is available, but it fails the selected rule or score threshold.\n"
            "- Error: no valid product/SMILES could be generated, or the reaction/sanitization failed.\n"
            "- Duplicates: Is_Duplicate and Duplicate_Of relative to the first repeated InChIKey.\n"
            "\n"
            "WHY THESE PARAMETERS?\n"
            "- MW/LogP/HBA/HBD/TPSA are standard descriptors used to estimate drug-likeness and permeability.\n"
            "- Lipinski/Ghose/Veber/Egan/Muegge are common heuristic filters for prioritization.\n"
            "\n"
            "SCORE / COMPATIBILITY (HEURISTIC) (%)\n"
            "- Computed with penalties for deviating from target values (LogP ~ 2.5, MW ~ 350, TPSA ~ 90).\n"
            "- Important: this is NOT a validated model of biological activity/ADMET; treat it as an internal heuristic ranking.\n"
            "- The 'Score threshold' slider discards results below the threshold (shown as Discarded with reason 'Below threshold').\n"
            "\n"
            "EXPORTS (overview)\n"
            "- Under the table: Export Table (CSV/Sheets/PDF), Export 3D ZIP, copy SMILES, and send candidates to ADMET local.\n"
            "- Export Table lets you choose Ideal / Warning / Error / Generated / All and the output format.\n"
            "- 3D ZIP exports generated candidates with SMILES (Ideal and Warning) through its own candidate selector.\n"
            "- ADMET (local) runs offline predictions and feeds the ADMET tab with integrated search and visualization.\n"
            "- In v1.1.0 (core), advanced packages (Custom ZIP / reproducible bundles / paper dataset / extra analytics) ship as plugins/packs.\n"
            "\n"
            "Failure_Reason\n"
            "- Explains the exact reason for discarding (e.g. 'No products generated', 'Sanitize failed', 'Invalid reactant', 'Fails <Rule>', 'Below threshold')."
        ),
        "results_help_workflow_title": "Platform workflow (summary)",
        "results_help_workflow": (
            "1) Select an MCR reaction and the 'Ideal criterion' (Engine tab).\n"
            "2) Upload one file per component (NAME, SMILES) and optionally select core reagents.\n"
            "3) The engine generates combinations (Cartesian product) and runs the reaction (SMARTS) with RDKit.\n"
            "4) (Optional) Standardize products (desalt/neutralize).\n"
            "5) For successful products, compute descriptors + compatibility (%) + Pass_* rules + MedChem alerts.\n"
            "6) Compute InChIKey and flag duplicates.\n"
            "7) Classify Ideal / Warning / Error using the selected criterion and record Failure_Reason.\n"
            "8) Results: filter Ideal / Warning / Error / Generated / All; use 'Custom…' for columns; 2D structure on row selection.\n"
            "9) Export as needed: table CSV/XLSX/PDF or 3D ZIP.\n"
            "10) For advanced functionality, use future packs/plugins."
        ),
        "results_help_views_title": "How to read Ideal / Warning / Error",
        "results_help_views": (
            "- Ideal: rows that satisfy the active 'Ideal criterion' on the Engine tab (not only Lipinski—you can change the rule).\n"
            "- Warning: generated structures with SMILES_Final that fail the criterion or threshold; review is under user responsibility.\n"
            "- Error: failed attempts without a valid generated product.\n"
            "- Generated: all rows with SMILES_Final (Ideal + Warning).\n"
            "- All: every evaluated attempt, consistent with the run's Total counter.\n"
            "\n"
            "FILTER-AWARE EXPORTS\n"
            "- Export Table lets you choose scope and format explicitly: CSV, Sheets (XLSX), or PDF.\n"
            "- 3D ZIP uses its own candidate selector and can include generated Warning structures with SMILES."
        ),
        "results_toggle_info_hide": "Hide info panels",
        "results_toggle_info_show": "Show info panels",
        "mcr_label": "MCR:", "data_preview": "Data Preview", "limpiar_todo": "✕  Clear All",
        "reiniciar": "↻  Restart", "resultados_limpiados": "Results cleared",
        "sin_datos": "No data loaded", "frecuencia": "Frequency", "desc_label": "Disc.",
        "producto": "Product", "no_preview": "No preview for this reaction",
        "restart_confirm": "Do you want to restart the entire application? Unsaved data will be lost.",
        "error_no_data": "No data to export.", "export_plots_title": "Export Plots",
        "missing_libraries": "Missing Libraries",
        "no_valid_products": "No valid products generated. Check SMILES or lower threshold.",
        "saved": "Saved:",
        "guide_title": "User Guide — Moleku",
        "guide_text": (
            "WELCOME TO Moleku v1.1.0\n"
            "──────────────────────────────\n"
            "Moleku is a desktop platform for Computer-Aided Drug Design (CADD), enabling rapid virtual library generation via Multi-Component Reactions (MCR).\n\n"
            "> STEP 1: PREPARE INPUT FILES\n"
            "Each file must contain exactly two columns: NAME (identifier) and SMILES (molecular structure).\n"
            "✅ Supported formats: .csv, .txt, .tsv, .dat, .smi, .xlsx, .xls, .ods, .json, .numbers\n"
            "🔍 Delimiters auto-detected: comma, semicolon, tab, space, or pipe.\n"
            "🧪 Accepted SMILES styles: canonical, lowercase aromatic, Kekule/non-aromatic, equivalent representations with different atom order, isomeric/stereochemical forms (`@`, `/`, `\\`), and RDKit-compatible CXSMILES.\n"
            "🗂 Single-column SMILES files are also accepted, along with common headers such as SMILES, Canonical_SMILES, Isomeric_SMILES, or CXSMILES.\n"
            "📄 Example structure:\n"
            "    NAME,SMILES\n"
            "    Benzaldehyde,c1ccccc1C=O\n"
            "    4-Nitrobenzaldehyde,O=Cc1ccc([N+](=O)[O-])cc1\n"
            "    Cinnamaldehyde_E,O=C/C=C/c1ccccc1\n\n"
            "> STEP 2: SELECT MCR REACTION\n"
            "In Moleku v1.1.0 (core) only three 3-component MCRs are included: Biginelli (3-CR), GBB (3-CR), and Gewald (3-CR). Ugi (4-CR) and other reactions are not part of this release. The Data Preview panel displays the reaction scheme, DOI, and mechanistic notes.\n"
            "⚗️ For reactions with fixed core components, use the checkboxes. Select one or multiple to automatically generate ALL combinatorial variations in a single run.\n\n"
            "> STEP 3: CONFIGURE & RUN\n"
            "Upload one file per external component. Adjust the Score threshold (0–100%). Click '▶ Start virtual generation'.\n"
            "⚙️ The engine computes the Cartesian product, maps RDKit SMARTS, and evaluates each product with scoring + drug-likeness rules (Lipinski/Ghose/Veber/Egan/Muegge).\n"
            "🧼 Optional: enable 'Standardize products' for desalt/neutralize and InChIKey-based deduplication.\n\n"
            "> STEP 4: ANALYZE RESULTS\n"
            "Results appear in 'Results'. Filter by Ideal / Warning / Error / Generated / All. Click any row to view 2D structure and properties.\n"
            "🧩 Use 'Custom…' to choose visible columns (works even before you have data, to preconfigure the table).\n"
            "Table headers follow the UI language; exported files keep stable internal column names.\n"
            "🧬 Chirality/stereochemistry: the table includes Has_Stereo and chiral center counts (defined/unassigned) computed from SMILES_Final.\n"
            "💾 Under the table: Export Table (CSV/Sheets/PDF), Export 3D ZIP, copy SMILES, and send generated candidates to the ADMET tab for local analysis.\n"
            "🧠 The ADMET tab behaves like an integrated search workspace: paste SMILES, import generated Ideal/Warning candidates, move through compounds with the search bar, and inspect local outputs without popups.\n"
            "🧪 The collapsible ADMET panels summarize how to load candidates, how to interpret predictions, and which workflow to follow for prioritization.\n"
            "🧩 ADMET exports support CSV/Sheets/PDF. 3D ZIP is available under the Results table and can include generated Warning structures with SMILES.\n"
            "⚠️ ADMET predictions are screening-oriented estimates and should not be treated as experimental proof.\n"
            "🧩 Other advanced exports (Custom ZIP, reproducible bundles, paper dataset, etc.) will ship as packs/plugins in future releases.\n"
            "💬 Use the 'Feedback' button (top-right) to suggest reactions/features and report issues.\n\n"
            "> STEP 5: EXPORT 3D ZIP\n"
            "Use Export 3D ZIP under the Results table to generate conformer SDF files for selected Ideal or Warning structures with SMILES.\n\n"
            "⚠️ TROUBLESHOOTING & BEST PRACTICES\n"
            "• 'No valid products': Lower threshold or verify SMILES validity.\n"
            "• RDKit errors: Run `conda install -c conda-forge rdkit`.\n"
            "• Apple .numbers files: Export to .xlsx/.csv if loading fails.\n"
            "• Keep files under 50,000 entries per component for optimal performance.\n\n"
            "- USE THE BUTTONS BELOW TO DOWNLOAD GENERIC TEMPLATES OR REACTION-SPECIFIC PACKS -.\n"
        ),
        "guide_templates_title": "Download Example Templates:",
        "guide_template_csv": "CSV Template (.csv)",
        "guide_template_txt": "TXT/TSV Template (.txt)",
        "guide_template_xlsx": "Sheets Template (.xlsx)",
        "guide_packs_title": "Reaction-ready Packs (.zip):",
        "guide_pack_biginelli": "Biginelli Pack",
        "guide_pack_gbb": "GBB Pack",
        "guide_pack_gewald": "Gewald Pack",
        "about_desc": "A desktop CADD platform for virtual library generation via 3-component MCRs (Biginelli, GBB, and Gewald) and compound prioritization using physicochemical descriptors, drug-likeness rules (Lipinski/Ghose/Veber/Egan/Muegge), InChIKey-based deduplication, and MedChem alerts (PAINS/Brenk). Exports CSV/Sheets/PDF and a 3D conformer ZIP to integrate with academic and industrial workflows.",
        "about_footer": "Dependencies: RDKit | Pandas | Pillow | CustomTkinter\nLicense: Apache License 2.0 • © 2026 Felipe Lizama Mora"
        ,
        # Web (Swiss-like) UI strings
        "web_title": "Moleku Web",
        "web_subtitle": "Web Platform",
        "web_nav_home": "Home",
        "web_nav_motor": "Engine",
        "web_nav_results": "Results",
        "web_nav_space": "Chemical space",
        "web_nav_guide": "Guide",
        "web_nav_about": "About",
        "web_welcome_title": "Welcome to Moleku",
        "web_welcome_subtitle": "Choose how you want to use the platform: web version or download the desktop app.",
        "web_welcome_open_web": "Open web platform",
        "web_welcome_download_desktop": "Download desktop app (GitHub)",
        "web_welcome_hint": "For the desktop app, GitHub hosts the code and (when available) the Releases/downloads section.",
        "web_welcome_card_web_title": "Web platform",
        "web_welcome_card_web_desc": "Run the engine, explore results, 2D/3D viewers, chemical space, and exports right from your browser.",
        "web_welcome_card_desktop_title": "Desktop app",
        "web_welcome_card_desktop_desc": "Get the project from GitHub to use the desktop version and its advanced tools.",
        "web_recommended": "Recommended",
        "web_links_title": "Links",
        "web_links_hint": "Quick access to profiles and institutions.",
        "web_inputs_title": "Inputs",
        "web_inputs_supported": "Supported: csv/tsv/txt/xlsx/json/numbers/ods/smi.",
        "web_histogram": "histogram",
        "web_plot_not_available": "Plot not available for this run.",
        "web_viewer2d_title": "2D viewer",
        "web_loading_2d": "Loading 2D viewer…",
        "web_download_3d_zip": "3D SDF (ZIP)",
        "web_kind": "kind",
        "web_row": "Row",
        "web_run": "Run",
        "web_status": "status",
        "web_progress": "progress",
        "web_all": "all",
        "web_run_log_qc": "Run log / QC",
        "web_run_setup_title": "Run setup",
        "web_run_setup_subtitle": "Upload one file per component, then run the engine.",
        "web_reaction_label": "Reaction (MCR)",
        "web_threshold_label": "Threshold",
        "web_ideal_rule_label": "Ideal rule",
        "web_standardize_label": "Standardize products (desalt/neutralize)",
        "web_run_btn": "Run",
        "web_results_title": "Results",
        "web_results_empty_hint": "Run the engine to see a structured report here (status, QC, counts, downloads).",
        "web_results_report_title": "Results report",
        "web_run_id": "Run ID",
        "web_new_run": "New run",
        "web_download_zip": "Download ZIP",
        "web_loading": "Loading…",
        "web_loading_table": "Loading table…",
        "web_loading_space": "Loading chemical space…",
        "web_loading_3d": "Loading 3D viewer…",
        "web_pending_table": "Waiting for results table…",
        "web_pending_space": "Waiting for chemical space…",
        "web_pending_3d": "Waiting for 3D viewer…",
        "web_recent_runs": "Recent runs",
        "web_recent_runs_hint": "Click to reopen a previous result.",
        "web_no_runs_yet": "No runs yet.",
        "web_results_table": "Results table",
        "web_view": "View",
        "web_section": "Section",
        "web_rows": "Rows",
        "web_filter_ph": "Filter (SMILES/InChIKey…)",
        "web_apply": "Apply",
        "web_page": "page",
        "web_no_rows": "No rows.",
        "web_showing_rows": "Showing {n} rows.",
        "web_prev": "Prev",
        "web_next": "Next",
        "web_space_title": "Chemical space",
        "web_space_desc": "PCA 2D on descriptors (MW/LogP/TPSA/HBA/HBD/RB/QED/Fsp3).",
        "web_download_pca_png": "Download PCA (PNG)",
        "web_download_pca_svg": "Download PCA (SVG)",
        "web_download_sdf": "Download SDF",
        "web_viewer3d_title": "3D viewer",
        "web_viewer3d_desc": "ETKDG + MMFF conformer rendered via 3Dmol.js.",
        "web_molecule": "Molecule",
        "web_notes": "Notes",
        "web_viewer3d_notes": "If a molecule fails 3D embedding, try another entry.",
        "web_no_molecules_3d": "No molecules available for 3D rendering.",
        "web_conformer_unavailable": "3D conformer unavailable for this entry",
        "web_core_reagents": "Core reagents",
        "web_core_reagents_hint": "Optional (defaults to the first option if none selected).",
        "web_no_results_yet_title": "No results yet",
        "web_no_results_yet_hint": "Go back to Motor and run a reaction.",
        "web_lang_label": "Language"
        ,
        "web_guide_title": "User Guide — Moleku Web",
        "web_guide_text": (
            "WELCOME TO Moleku WEB\n"
            "──────────────────────────────\n"
            "Moleku Web is the browser-accessible version. It mirrors the desktop workflow, with a web-adapted UI and navigation.\n\n"
            "STEP 1: PREPARE INPUT FILES\n"
            "Each file must contain two columns: NAME (identifier) and SMILES (structure).\n"
            "Common formats: CSV/TSV/TXT/XLSX. For Apple .numbers, export to .csv or .xlsx.\n\n"
            "STEP 2: SELECT REACTION (MCR)\n"
            "Pick the reaction and upload one file per component.\n"
            "If core reagents exist, you can select one or multiple to generate combinations.\n\n"
            "STEP 3: CONFIGURE & RUN\n"
            "Set threshold and Ideal rule. Click Run and wait until status becomes 'done'.\n\n"
            "STEP 4: RESULTS / SPACE / 3D\n"
            "Explore the table by sections, filter, and export CSV/ZIP. In Chemical Space, download PCA (PNG/SVG). In 3D, select molecules for inspection.\n\n"
            "TEMPLATES\n"
            "Use the download buttons to get ready-to-fill templates."
        ),
        "web_about_desc": (
            "Moleku Web (Multi Component Reaction Generator) is the web version of the platform for generating and analyzing virtual libraries based on MCRs "
            "for early drug discovery workflows. It reuses the same computational core (RDKit + pandas) and provides results, visualization (PCA/3D), "
            "and reproducible exports from the browser."
        ),
        "web_link_linkedin": "LinkedIn",
        "web_link_github": "GitHub",
        "web_link_sbbcs": "SB&BCS Lab",
        "web_link_ufro": "UFRO",
        "web_templates_title": "Example templates",
        "web_templates_hint": "Download templates (NAME,SMILES) for each component and fill your libraries.",
        "web_download_template_csv": "Download template (CSV)",
        "web_download_template_smi": "Download template (SMI)"
        ,
        "web_admet_title": "ADMET-IA",
        "web_admet_hint": "Copy SMILES and paste them into ADMET-IA (web) for predictions.",
        "web_copy_smiles_all": "Copy SMILES (All)",
        "web_copy_smiles_ideal": "Copy SMILES (Ideal)",
        "web_open_admet": "Open ADMET-IA (web)",
        "web_copied": "Copied to clipboard.",
        "web_plots_title": "Plots (distributions)",
        "web_plots_hint": "Quick histograms for inspection (exportable as PNG).",
        "web_plot_score": "Score",
        "web_plot_mw": "MW",
        "web_plot_logp": "LogP",
        "web_plot_tpsa": "TPSA",
        "web_download_png": "Download PNG",
        "web_plot_settings": "Plot Settings",
        "web_ps_color_ideal": "Color (Ideal)",
        "web_ps_color_discard": "Color (Discarded)",
        "web_ps_plot_bg": "Background",
        "web_ps_axis_color": "Axis color",
        "web_ps_grid_color": "Grid color",
        "web_ps_font_size": "Font size",
        "web_ps_font_bold": "Bold title",
        "web_ps_marker_size": "Marker size (PCA)",
        "web_ps_hist_bins": "Histogram bins",
        "web_ps_axis_width": "Axis width",
        "web_ps_grid_width": "Grid width",
        "web_ps_show_grid": "Show grid",
        "web_ps_show_legend": "Show legend",
        "web_ps_legend_pos": "Legend position",
        "web_ps_reset": "Reset",
        "web_ps_hint": "Tip: use hex colors (#RRGGBB). Saved in your browser."
    },
    # ──────────────────────────────────────────────────────────────────
    # Additional UI languages (v1.1.0): partial translations + English fallback
    # ──────────────────────────────────────────────────────────────────
    "Deutsch": {
        # Core navigation
        "titulo": "Moleku v1.1.0",
        "tab_motor": "Engine {rxn}",
        "tab_resultados": "Ergebnisse",
        "tab_admet": "ADMET",
        "tab_guide": "Anleitung",
        "tab_acerca": "Über",
        "feedback": "Feedback",

        # Motor
        "info_formato": "ℹ Formate: .csv, .txt, .tsv, .xlsx, .xls, .ods, .json, .numbers  |  Spalten: NAME und SMILES",
        "mcr_label": "MCR:",
        "data_preview": "Datenvorschau",
        "csv_de": "Datei für {comp}:",
        "examinar": "Durchsuchen…",
        "reactivos_centrales": "Zentrale Reagenzien:",
        "core_reagents_select_hint": "eins oder mehrere auswählen",
        "core_reagents_selected": "Ausgewählt",
        "core_reagents_selected_none": "keine",
        "core_reagents_tip": "Wähle mehrere Reagenzien, um ALLE Kombinationen in einem Lauf zu erzeugen.",
        "umbral": "Score-Schwelle (%):",
        "ideal_rule": "Ideal-Kriterium:",
        "standardize": "Produkte standardisieren (entsalzen/neutralisieren)",
        "iniciar": "▶  Virtuelle Generierung starten",
        "limpiar": "✕  Liste leeren",
        "procesando": "Verarbeitung…",
        "listo": "Fertig.",
        "error_archivos": "Bitte alle Dateien laden.",
        "missing_libraries": "Fehlende Bibliotheken",
        "no_valid_products": "Keine gültigen Produkte erzeugt. Prüfe SMILES oder senke die Schwelle.",

        # Results / exports
        "exportar_csv": "CSV exportieren",
        "exportar_xlsx": "XLSX exportieren",
        "exportar_pdf": "PDF exportieren",
        "exportar_zip": "3D-ZIP exportieren",
        "no_datos": "Keine Daten.",
        "saved": "Gespeichert:",
        "registros": "Einträge",
        "table_view_custom": "Benutzerdefiniert…",
        "table_cols_title": "Tabellenspalten",
        "table_cols_apply": "Anwenden",
        "table_cols_cancel": "Abbrechen",
        "results_toggle_info_hide": "Info-Panels ausblenden",
        "results_toggle_info_show": "Info-Panels anzeigen",

        # ADMET web
        "admet_open_web": "ADMET-IA öffnen (Web)",
        "admet_copy_sel": "SMILES kopieren (Auswahl)",
        "admet_copy_ideal": "SMILES kopieren (Ideal)",
        "admet_no_selection": "Bitte eine oder mehrere Zeilen auswählen.",
        "admet_missing_pkg_app": "Lokales ADMET ist in dieser ausführbaren Datei nicht korrekt verfügbar.\n\nBitte die aktualisierte Moleku-Version verwenden oder die App mit vollständiger ADMET-Laufzeit neu bauen.",
        "admet_export_csv": "ADMET exportieren (CSV)",
        "admet_tab_hint": "Füge in diesem Reiter ein oder mehrere SMILES ein oder lade Ideal-Kandidaten direkt aus den Ergebnissen, um lokale ADMET-Vorhersagen in einem suchbasierten Workflow zu untersuchen.",
        "admet_tab_input_title": "Kandidateneingabe",
        "admet_tab_input_hint": "Füge pro Zeile ein SMILES ein, nutze die Suche für bereits berechnete Kandidaten oder importiere die von Moleku erzeugten Ideal-Kandidaten.",
        "admet_info_title": "ADMET-Kurzhilfe",
        "admet_info_hint": "Kurze Panels zum Laden von Kandidaten, zur Interpretation der Ausgaben und zum Export nützlicher Teilmengen aus ADMET.",
        "admet_tab_run_input": "Eingefügte SMILES ausführen",
        "admet_tab_use_ideal": "Ideal-Ergebnisse verwenden",
        "admet_tab_search": "Kandidat/SMILES suchen:",
        "admet_tab_search_clear": "Leeren",
        "admet_tab_results_count": "Analysierte Kandidaten: {n} / {total}",
        "admet_tab_no_predictions": "Noch keine integrierten ADMET-Vorhersagen vorhanden.",
        "admet_tab_select_candidate": "Suche einen Kandidaten oder starte Vorhersagen, um Struktur und ADMET-Ausgaben anzuzeigen.",
        "admet_tab_candidate_title_empty": "2D-Viewer",
        "admet_tab_candidate_title": "Anzeige: {candidate}",
        "admet_tab_candidate_smiles": "SMILES: {smiles}",
        "admet_tab_summary_title_empty": "Ausgewählte ADMET-Ausgaben",
        "admet_tab_summary_title": "Ausgewählte ADMET-Ausgaben — {candidate}",
        "admet_tab_summary_empty": "Die ADMET-Ausgaben des ausgewählten Kandidaten erscheinen hier.",
        "admet_tab_no_input_smiles": "Bitte füge mindestens ein gültiges SMILES in das ADMET-Eingabefeld ein.",
        "admet_tab_no_ideal_results": "Keine Ideal-Kandidaten zum Senden an ADMET vorhanden.",
        "admet_tab_running": "Lokales ADMET wird für {n} Kandidat(en) berechnet...",
        "admet_help_input_title": "Kandidaten laden",
        "admet_help_input": (
            "• SMILES können direkt oben rechts eingefügt werden, jeweils eine Zeile pro Kandidat.\n"
            "• Auch Name/SMILES-Paare mit Tab, Komma oder Semikolon werden akzeptiert.\n"
            "• Zeilen mit '#' werden als Kommentare ignoriert und doppelte SMILES vor dem Lauf entfernt.\n"
            "• Zusätzlich lassen sich Ideal-Kandidaten direkt aus den Ergebnissen importieren.\n"
            "• Die Suchleiste filtert bereits berechnete Kandidaten nach Name oder SMILES, ohne ADMET neu zu starten."
        ),
        "admet_help_outputs_title": "ADMET-Ausgaben lesen",
        "admet_help_outputs": (
            "• Der 2D-Viewer zeigt die Struktur des aktiven Kandidaten.\n"
            "• 'Ausgewählte ADMET-Ausgaben' listet die lokalen Vorhersagen für diesen Kandidaten.\n"
            "• Viewer und Ausgabepanel aktualisieren sich beim Wechsel des Kandidaten innerhalb derselben Ansicht.\n"
            "• Diese Werte dienen der frühen Priorisierung und ersetzen keine experimentelle Validierung.\n"
            "• Häufige Warnzeichen sind sehr schlechte Permeabilität, hohe vorhergesagte Toxizität oder widersprüchliche Profile ähnlicher Kandidaten."
        ),
        "admet_help_workflow_title": "Empfohlener ADMET-Workflow",
        "admet_help_workflow": (
            "1) Generiere Kandidaten in Moleku oder füge einen externen SMILES-Satz ein.\n"
            "2) Starte lokales ADMET in diesem Reiter.\n"
            "3) Nutze die Suche oben, um schnell zwischen berechneten Kandidaten zu wechseln.\n"
            "4) Vergleiche 2D-Struktur und ADMET-Ausgaben, um beste und schwächste Profile zu priorisieren.\n"
            "5) Exportiere ADMET-CSV oder 3D-ZIP für alle Ideal-Kandidaten oder eine manuell gewählte Teilmenge.\n"
            "6) Behalte die stärksten Kandidaten für tiefergehende Analysen oder externe Validierung."
        ),
        "export_select_title_3d": "Kandidaten für 3D-ZIP auswählen",
        "export_select_title_admet": "Kandidaten für ADMET-Export auswählen",
        "export_select_hint": "Wähle, ob alle Ideal-Kandidaten oder eine manuell definierte Teilmenge exportiert werden soll.",
        "export_select_mode_ideal": "Alle Ideal-Kandidaten exportieren",
        "export_select_mode_manual": "Bestimmte Kandidaten manuell auswählen",
        "export_select_candidates": "Verfügbare Kandidaten",
        "export_select_all": "Alle auswählen",
        "export_select_clear": "Auswahl löschen",
        "export_select_apply": "Exportieren",
        "export_select_cancel": "Abbrechen",
        "export_select_need_candidates": "Keine Kandidaten zum Export verfügbar.",
        "export_select_need_manual": "Bitte wähle mindestens einen Kandidaten zum Export aus.",

        # Chirality labels (panel keys)
        "stats_has_stereo": "Stereochemie",
        "stats_chiral_centers": "Chirale Zentren",

        # Info panels (Results)
        "results_help_params_title": "Was bedeuten diese Parameter?",
        "results_help_params": (
            "• Heuristische Kompatibilität (%): 0–100 Score aus LogP, MW und TPSA (höher ist besser unter diesem Modell).\n"
            "• MW: Molekulargewicht (Da).\n"
            "• LogP: Lipophilie (RDKit-Schätzung).\n"
            "• TPSA: topologische polare Oberfläche.\n"
            "• HBA/HBD: H‑Brücken‑Akzeptoren/Donoren.\n"
            "• Rotierbare Bindungen, schwere Atome, Ringzahl, molare Refraktivität: zusätzliche Strukturdeskriptoren.\n"
            "• QED/Fsp3: globale Drug‑Likeness‑Heuristiken.\n"
            "• PAINS/Brenk: strukturelle Alert‑Heuristiken (ersetzen keine Expertenbewertung).\n"
            "• InChIKey: Standard‑Identifier zur Duplikaterkennung.\n"
            "• Stereochemie/Chiralität:\n"
            "  - Has_Stereo: True, wenn SMILES Stereo codiert (chirale Zentren oder E/Z).\n"
            "  - Chiral_Centers: Anzahl chiraler Zentren (RDKit).\n"
            "  - Unassigned: chirale Zentren vorhanden, aber ohne R/S‑Zuordnung.\n"
            "\n"
            "KLASSIFIKATION (Ideal vs Discarded)\n"
            "- Ideal: hängt vom gewählten Ideal‑Kriterium ab (Lipinski / Ghose / Veber / Egan / Muegge / Any / All).\n"
            "- Discarded: Produkt scheitert am Kriterium oder an der Score‑Schwelle, oder es wurde kein gültiges Produkt erzeugt.\n"
            "\n"
            "EXPORTS (Übersicht)\n"
            "- Unter der Tabelle: CSV, XLSX, PDF und 3D‑ZIP; SMILES kopieren; ADMET‑IA (Web/lokal).\n"
            "- NEU: CSV, XLSX und PDF berücksichtigen den aktiven Tabellenfilter (Ideal / All / Discard) – die Datei enthält exakt die sichtbaren Zeilen, keine Leerstellen. Der vorgeschlagene Dateiname enthält den Filter (z. B. mcrg_results_ideal.csv).\n"
            "- 3D‑ZIP folgt seiner eigenen Logik (immer Konformere der Ideal‑Verbindungen), da 3D‑Erzeugung aufwendig ist und sich auf priorisierte Kandidaten konzentriert.\n"
            "- ADMET‑IA: 'ADMET‑IA öffnen (Web)' nutzt das Webportal; 'ADMET (lokal)' führt Offline‑Vorhersagen aus, wenn das optionale Paket 'admet-ai' installiert ist (pip install admet-ai).\n"
            "- Erweiterte Pakete (Custom ZIP / reproduzierbare Bundles / Paper‑Dataset / Extra‑Analysen) kommen als Plugins/Packs.\n"
        ),
        "results_help_workflow_title": "Workflow (Kurzfassung)",
        "results_help_workflow": (
            "1) Wähle eine MCR‑Reaktion und das Ideal‑Kriterium.\n"
            "2) Lade pro Komponente eine Datei (NAME, SMILES).\n"
            "3) Der Motor erzeugt Kombinationen (kartesisches Produkt) und führt die Reaktion (SMARTS) mit RDKit aus.\n"
            "4) Optional: Standardisierung (entsalzen/neutralisieren).\n"
            "5) Deskriptoren + Score + Regeln (Pass_*) + MedChem‑Alerts.\n"
            "6) InChIKey berechnen und Duplikate markieren.\n"
            "7) Ideal/Discarded klassifizieren und Failure_Reason setzen.\n"
            "8) Ergebnisse filtern; 'Benutzerdefiniert…' für Spalten; 2D‑Viewer per Auswahl.\n"
            "9) Export: CSV/XLSX/PDF/3D‑ZIP.\n"
        ),
        "results_help_views_title": "Ideal / All / Discard verstehen",
        "results_help_views": (
            "- Ideal: erfüllt das aktive Ideal‑Kriterium.\n"
            "- Discard: fehlgeschlagene Versuche oder Produkte, die Kriterium/Schwelle nicht erfüllen (SMILES_Final kann trotzdem vorhanden sein).\n"
            "- All: alle ausgewerteten Versuche (Ideal + Discard).\n"
            "\n"
            "FILTERABHÄNGIGER EXPORT\n"
            "- CSV, Sheets (XLSX) und PDF exportieren exakt die aktive Ansicht (Ideal / All / Discard); Filtern vor dem Export vermeidet Leerzeilen.\n"
            "- 3D‑ZIP nutzt diesen Filter nicht: es werden stets nur die als Ideal klassifizierten Verbindungen exportiert (3D‑Erzeugung ist aufwendig).\n"
        ),

        # Guide/About
        "guide_title": "Benutzerhandbuch — Moleku",
        # Full guide content (same information as Spanish/English, translated)
        "guide_text": (
            "WILLKOMMEN BEI Moleku v1.1.0\n"
            "──────────────────────────────\n"
            "Moleku ist eine professionelle Desktop-Plattform für Computer-Aided Drug Design (CADD) und ermöglicht die schnelle Generierung virtueller Bibliotheken über Multi-Component Reactions (MCR).\n\n"
            "> SCHRITT 1: EINGABEDATEIEN VORBEREITEN\n"
            "Jede Datei muss genau zwei Spalten enthalten: NAME (Bezeichner) und SMILES (molekulare Struktur).\n"
            "✅ Unterstützte Formate: .csv, .txt, .tsv, .dat, .smi, .xlsx, .xls, .ods, .json, .numbers\n"
            "🔍 Trennzeichen werden automatisch erkannt: Komma, Semikolon, Tab, Leerzeichen oder Pipe.\n"
            "🧪 Unterstützte SMILES-Stile: kanonisch, aromatisch in Kleinbuchstaben, Kekulé/nicht-aromatisch, äquivalente Darstellungen mit anderer Atomreihenfolge, isomere/stereochemische Formen (`@`, `/`, `\\`) und RDKit-kompatibles CXSMILES.\n"
            "🗂 Auch Ein-Spalten-SMILES-Dateien sowie gängige Header wie SMILES, Canonical_SMILES, Isomeric_SMILES oder CXSMILES werden akzeptiert.\n"
            "📄 Beispiel:\n"
            "    NAME,SMILES\n"
            "    Benzaldehyd,c1ccccc1C=O\n"
            "    4-Nitrobenzaldehyd,O=Cc1ccc([N+](=O)[O-])cc1\n"
            "    Zimtaldehyd_E,O=C/C=C/c1ccccc1\n\n"
            "> SCHRITT 2: MCR-REAKTION AUSWÄHLEN\n"
            "In Moleku v1.1.0 (core) sind ausschließlich drei 3-Komponenten-MCRs enthalten: Biginelli (3-CR), GBB (3-CR) und Gewald (3-CR). Ugi (4-CR) und weitere Reaktionen gehören nicht zu dieser Version. Das Vorschau-Panel zeigt Schema, DOI und Hinweise.\n"
            "⚗️ Bei Reaktionen mit festen zentralen Komponenten nutzt du die Checkboxen (Zentrale Reagenzien), um Varianten zu erzeugen.\n\n"
            "> SCHRITT 3: KONFIGURIEREN & STARTEN\n"
            "Lade je Komponente eine Datei hoch. Stelle die Score-Schwelle (0–100%) ein und klicke auf '▶ Virtuelle Generierung starten'.\n"
            "⚙️ Der Motor bildet das kartesische Produkt, mappt SMARTS mit RDKit und bewertet Produkte über Score + Drug-Likeness-Regeln (Lipinski/Ghose/Veber/Egan/Muegge).\n"
            "🧼 Optional: 'Produkte standardisieren' (Entsalzen/Neutralisieren) sowie Duplikaterkennung per InChIKey.\n\n"
            "> SCHRITT 4: ERGEBNISSE ANALYSIEREN\n"
            "Ergebnisse erscheinen unter 'Ergebnisse'. Filter: Ideal / All / Discarded. Klicke eine Zeile für 2D-Struktur und Eigenschaften.\n"
            "🧩 'Benutzerdefiniert…' wählt sichtbare Spalten (auch ohne Daten).\n"
            "🧬 Stereochemie/Chiralität: Has_Stereo und die Anzahl chiraler Zentren (definiert/undefiniert) werden aus SMILES_Final berechnet.\n"
            "💾 Unter der Tabelle: CSV/XLSX/PDF exportieren, SMILES kopieren und Kandidaten an den ADMET-Reiter senden.\n"
            "🧠 Der ADMET-Reiter arbeitet wie ein integrierter Such-Arbeitsbereich: SMILES einfügen, Ideal-Kandidaten importieren, Kandidaten per Suche wechseln und lokale Ausgaben ohne Popups prüfen.\n"
            "🧪 Die einklappbaren ADMET-Panels erklären Kandidaten-Import, Interpretation der Vorhersagen und den empfohlenen Priorisierungs-Workflow.\n"
            "🧩 3D-ZIP und ADMET-CSV werden nun im ADMET-Reiter gestartet; beide erlauben den Export aller Ideal-Kandidaten oder einer manuell gewählten Teilmenge.\n"
            "⚠️ ADMET-Vorhersagen sind Hilfsmittel für das frühe Screening und ersetzen keine experimentellen Daten.\n"
            "💬 Nutze 'Feedback' (oben rechts) für Wünsche/Fehlerberichte.\n\n"
            "> SCHRITT 5: 3D-ZIP EXPORT\n"
            "Exportiere aus dem ADMET-Reiter ein 3D-ZIP mit Konformeren (SDF) oder eine ADMET-CSV für alle Ideal-Kandidaten oder eine manuell gewählte Teilmenge.\n\n"
            "⚠️ FEHLERSUCHE & BEST PRACTICES\n"
            "• 'Keine gültigen Produkte': Schwelle senken oder SMILES prüfen.\n"
            "• RDKit-Fehler: `conda install -c conda-forge rdkit`.\n"
            "• Apple .numbers: bei Problemen nach .xlsx/.csv exportieren.\n"
            "• Für Performance: Dateien < 50.000 Einträge pro Komponente.\n\n"
            "- NUTZE DIE BUTTONS UNTEN, UM VORLAGEN HERUNTERZULADEN -.\n"
        ),
        "guide_templates_title": "Beispielvorlagen herunterladen:",
        "guide_template_csv": "CSV-Vorlage (.csv)",
        "guide_template_txt": "TXT/TSV-Vorlage (.txt)",
        "guide_template_xlsx": "Sheets-Vorlage (.xlsx)",
        "guide_packs_title": "Reaktionsfertige Packs (.zip):",
        "guide_pack_biginelli": "Biginelli-Pack",
        "guide_pack_gbb": "GBB-Pack",
        "guide_pack_gewald": "Gewald-Pack",
        "about_desc": "Eine Desktop-CADD-Plattform zur virtuellen Bibliotheksgenerierung via 3-Komponenten-MCRs (Biginelli, GBB, Gewald) und Priorisierung mittels Deskriptoren, Drug‑Likeness‑Regeln (Lipinski/Ghose/Veber/Egan/Muegge), InChIKey‑Duplikaten, MedChem‑Alerts (PAINS/Brenk) sowie Export (CSV/XLSX/PDF/3D‑ZIP).",
    },
    "日本語": {
        # Core navigation
        "titulo": "Moleku v1.1.0",
        "tab_motor": "エンジン {rxn}",
        "tab_resultados": "結果",
        "tab_guide": "ガイド",
        "tab_acerca": "概要",
        "feedback": "フィードバック",

        # Motor
        "info_formato": "ℹ 形式: .csv, .txt, .tsv, .xlsx, .xls, .ods, .json, .numbers  |  列: NAME と SMILES",
        "mcr_label": "MCR:",
        "data_preview": "データプレビュー",
        "csv_de": "{comp} ファイル:",
        "examinar": "参照…",
        "reactivos_centrales": "中心試薬:",
        "core_reagents_select_hint": "1つ以上を選択",
        "core_reagents_selected": "選択",
        "core_reagents_selected_none": "なし",
        "core_reagents_tip": "複数の試薬を選ぶと、1回の実行で全組合せを生成できます。",
        "umbral": "スコアしきい値 (%):",
        "ideal_rule": "Ideal 基準:",
        "standardize": "生成物を標準化（脱塩/中和）",
        "iniciar": "▶  生成を開始",
        "limpiar": "✕  リストをクリア",
        "procesando": "処理中…",
        "listo": "完了。",
        "error_archivos": "すべてのファイルを読み込んでください。",
        "missing_libraries": "ライブラリ不足",
        "no_valid_products": "有効な生成物がありません。SMILES を確認するか、しきい値を下げてください。",

        # Results / exports
        "exportar_csv": "CSV 書き出し",
        "exportar_xlsx": "XLSX 書き出し",
        "exportar_pdf": "PDF 書き出し",
        "exportar_zip": "3D ZIP 書き出し",
        "no_datos": "データなし。",
        "saved": "保存先:",
        "registros": "件",
        "table_view_custom": "カスタム…",
        "table_cols_title": "表の列",
        "table_cols_apply": "適用",
        "table_cols_cancel": "キャンセル",
        "results_toggle_info_hide": "情報パネルを隠す",
        "results_toggle_info_show": "情報パネルを表示",

        # ADMET web
        "admet_open_web": "ADMET-IA（Web）を開く",
        "admet_copy_sel": "SMILES をコピー（選択）",
        "admet_copy_ideal": "SMILES をコピー（Ideal）",
        "admet_no_selection": "表で行を選択してください。",
        "tab_admet": "ADMET",
        "admet_missing_pkg_app": "この実行ファイルではローカル ADMET が正しく利用できません。\n\n更新済みの Moleku ビルドを使用するか、完全な ADMET ランタイムを含めて再ビルドしてください。",
        "admet_export_csv": "ADMET を書き出し (CSV)",
        "admet_tab_hint": "このタブに SMILES を貼り付けるか、結果から Ideal 候補を読み込み、検索ベースのワークフローでローカル ADMET 予測を確認します。",
        "admet_tab_input_title": "候補入力",
        "admet_tab_input_hint": "1 行につき 1 つの SMILES を貼り付け、検索バーで既計算候補を参照するか、Moleku で生成された Ideal 候補を読み込みます。",
        "admet_info_title": "ADMET クイックガイド",
        "admet_info_hint": "候補の読み込み方法、出力の見方、ADMET から有用な部分集合をエクスポートする方法を短く説明します。",
        "admet_tab_run_input": "貼り付けた SMILES を実行",
        "admet_tab_use_ideal": "Ideal 結果を使用",
        "admet_tab_search": "候補/SMILES を検索:",
        "admet_tab_search_clear": "クリア",
        "admet_tab_results_count": "解析済み候補: {n} / {total}",
        "admet_tab_no_predictions": "統合された ADMET 予測はまだありません。",
        "admet_tab_select_candidate": "候補を検索するか予測を実行して、構造と ADMET 出力を表示します。",
        "admet_tab_candidate_title_empty": "2D ビューア",
        "admet_tab_candidate_title": "表示中: {candidate}",
        "admet_tab_candidate_smiles": "SMILES: {smiles}",
        "admet_tab_summary_title_empty": "選択した ADMET 出力",
        "admet_tab_summary_title": "選択した ADMET 出力 — {candidate}",
        "admet_tab_summary_empty": "選択した候補の ADMET 出力がここに表示されます。",
        "admet_tab_no_input_smiles": "ADMET 入力欄に少なくとも 1 つの有効な SMILES を入力してください。",
        "admet_tab_no_ideal_results": "ADMET に送信できる Ideal 候補がありません。",
        "admet_tab_running": "{n} 件の候補に対してローカル ADMET を計算中...",
        "admet_help_input_title": "候補の読み込み方法",
        "admet_help_input": (
            "• 右上の入力欄に SMILES を 1 行ずつ直接貼り付けできます。\n"
            "• タブ、カンマ、セミコロン区切りの名前/SMILES ペアも受け付けます。\n"
            "• '#' で始まる行はコメントとして無視され、重複 SMILES は実行前に除去されます。\n"
            "• 結果タブから Ideal 候補のみを直接読み込むこともできます。\n"
            "• 検索バーはすでに計算済みの候補を名前または SMILES で絞り込み、再計算は行いません。"
        ),
        "admet_help_outputs_title": "ADMET 出力の見方",
        "admet_help_outputs": (
            "• 2D ビューアには現在の候補の構造が表示されます。\n"
            "• 「選択した ADMET 出力」にはその候補のローカル予測結果が並びます。\n"
            "• 候補を切り替えると、ビューアと出力パネルは同じタブ内で更新されます。\n"
            "• これらの値は初期スクリーニングの優先順位付けに役立ちますが、実験検証を置き換えるものではありません。\n"
            "• 典型的な注意点として、極端に低い透過性、高い予測毒性、類似候補間で矛盾するプロファイルが挙げられます。"
        ),
        "admet_help_workflow_title": "推奨 ADMET ワークフロー",
        "admet_help_workflow": (
            "1) Moleku で候補を生成するか、外部の SMILES バッチを貼り付けます。\n"
            "2) このタブからローカル ADMET を実行します。\n"
            "3) 上部の検索バーで計算済み候補を素早く切り替えます。\n"
            "4) 2D 構造と ADMET 出力を比較して、良い/悪いプロファイルを順位付けします。\n"
            "5) ADMET CSV または 3D ZIP を、すべての Ideal 候補または手動選択した部分集合に対して出力します。\n"
            "6) 有望な候補を詳細解析や外部検証に進めます。"
        ),
        "export_select_title_3d": "3D ZIP 用候補を選択",
        "export_select_title_admet": "ADMET 出力候補を選択",
        "export_select_hint": "すべての Ideal 候補を出力するか、特定の候補だけを手動で選ぶかを選択します。",
        "export_select_mode_ideal": "すべての Ideal 候補を出力",
        "export_select_mode_manual": "候補を手動で選択",
        "export_select_candidates": "利用可能な候補",
        "export_select_all": "すべて選択",
        "export_select_clear": "選択解除",
        "export_select_apply": "出力",
        "export_select_cancel": "キャンセル",
        "export_select_need_candidates": "出力可能な候補がありません。",
        "export_select_need_manual": "少なくとも 1 つの候補を選択してください。",

        # Chirality labels (panel keys)
        "stats_has_stereo": "立体化学",
        "stats_chiral_centers": "不斉中心",

        # Info panels (Results)
        "results_help_params_title": "これらのパラメータの意味",
        "results_help_params": (
            "• 互換性スコア（%）: LogP/MW/TPSA から計算される 0–100 の指標（高いほど良い）。\n"
            "• MW: 分子量（Da）。\n"
            "• LogP: 疎水性（RDKit 推定）。\n"
            "• TPSA: トポロジカル極性表面積。\n"
            "• HBA/HBD: 水素結合受容体/供与体。\n"
            "• その他: 回転結合数、重原子数、環数、モル屈折率など。\n"
            "• PAINS/Brenk: 構造アラート（参考指標）。\n"
            "• InChIKey: 重複検出に使用。\n"
            "• 立体化学/キラリティ:\n"
            "  - Has_Stereo: SMILES に立体情報（@ や E/Z）が含まれる場合 True。\n"
            "  - Chiral_Centers: RDKit が検出した不斉中心数。\n"
            "  - Unassigned: 不斉中心があるが R/S が未指定。\n"
            "\n"
            "分類（Ideal / Discard）\n"
            "- Ideal: 選択した Ideal 基準を満たす。\n"
            "- Discard: 基準/しきい値を満たさない、または生成失敗。\n"
            "\n"
            "エクスポート\n"
            "- 表の下: CSV/XLSX/PDF/3D ZIP、SMILES コピー、ADMET‑IA（Web/ローカル）。\n"
            "- 新機能: CSV/XLSX/PDF は現在のテーブルフィルタ（Ideal / All / Discard）に従って出力されます。表示中の行と完全に一致し、空白セルは生成されません。推奨ファイル名にはフィルタ名が含まれます（例: mcrg_results_ideal.csv）。\n"
            "- 3D ZIP は従来通り、Ideal と分類された化合物の 3D コンフォーマーのみを出力します（3D 生成はコストが高いため）。\n"
            "- ADMET‑IA: 'ADMET-IA を開く（Web）' は Web ポータルを利用。'ADMET (ローカル)' はオプションの 'admet-ai' パッケージがインストールされていればオフラインで予測を実行します（pip install admet-ai）。\n"
            "- 高度な機能は今後 packs/plugins として提供。\n"
        ),
        "results_help_workflow_title": "ワークフロー（概要）",
        "results_help_workflow": (
            "1) 反応と Ideal 基準を選択。\n"
            "2) 成分ごとに NAME/SMILES ファイルを読み込む。\n"
            "3) 組合せ生成（直積）→ RDKit SMARTS で反応。\n"
            "4) 任意: 標準化。\n"
            "5) 記述子・スコア・ルール・アラートを計算。\n"
            "6) InChIKey で重複をマーク。\n"
            "7) Ideal/Discard を分類。\n"
            "8) 結果フィルタ、列カスタム、2D 表示。\n"
            "9) CSV/XLSX/PDF/3D ZIP を出力。\n"
        ),
        "results_help_views_title": "Ideal / All / Discard の見方",
        "results_help_views": (
            "- Ideal: 基準を満たす行。\n"
            "- Discard: 失敗または基準/しきい値未満（SMILES_Final が残る場合あり）。\n"
            "- All: すべての評価行。\n"
            "\n"
            "フィルタ連動エクスポート\n"
            "- CSV/Sheets (XLSX)/PDF は現在のビュー（Ideal / All / Discard）のみを出力します。エクスポート前にフィルタを設定すると空白行を避けられます。\n"
            "- 3D ZIP はこのフィルタを使用せず、Ideal と分類された化合物のみを常に出力します（3D 生成のコストが高いため）。\n"
        ),

        # Guide/About
        "guide_title": "ユーザーガイド — Moleku",
        "guide_text": (
            "Moleku v1.1.0 へようこそ\n"
            "──────────────────────────────\n"
            "Moleku は多成分反応（MCR）により仮想ライブラリを迅速に生成する、プロフェッショナルなデスクトップ CADD プラットフォームです。\n\n"
            "> ステップ 1: 入力ファイルの準備\n"
            "各ファイルは NAME（識別子）と SMILES（構造）の 2 列が必須です。\n"
            "✅ 対応形式: .csv, .txt, .tsv, .dat, .smi, .xlsx, .xls, .ods, .json, .numbers\n"
            "🔍 区切り文字は自動判定（カンマ/セミコロン/タブ/スペース/パイプ）。\n"
            "🧪 対応する SMILES 形式: canonical、芳香族小文字表記、Kekulé/非芳香族、原子順が異なる等価表現、異性体/立体化学表現（`@`, `/`, `\\`）、RDKit 互換の CXSMILES。\n"
            "🗂 単一列の SMILES ファイルや、SMILES / Canonical_SMILES / Isomeric_SMILES / CXSMILES といった一般的なヘッダも利用できます。\n"
            "📄 例:\n"
            "    NAME,SMILES\n"
            "    Benzaldehyde,c1ccccc1C=O\n"
            "    4-Nitrobenzaldehyde,O=Cc1ccc([N+](=O)[O-])cc1\n"
            "    Cinnamaldehyde_E,O=C/C=C/c1ccccc1\n\n"
            "> ステップ 2: MCR 反応の選択\n"
            "v1.1.0（core）では 3 成分 MCR のみ 3 つ（Biginelli (3-CR)、GBB (3-CR)、Gewald (3-CR)）を提供します。Ugi (4-CR) などはこの版の対象外です。プレビューにスキーム/DOI/注意点が表示されます。\n"
            "⚗️ 中心成分がある反応では、チェックボックス（中心試薬）で組合せを生成できます。\n\n"
            "> ステップ 3: 設定して実行\n"
            "成分ごとにファイルを読み込み、スコアしきい値（0–100%）を設定して開始します。\n"
            "⚙️ 直積で組合せを生成し、RDKit SMARTS で反応を実行、スコアと Drug-likeness ルールで評価します。\n"
            "🧼 任意: 標準化（脱塩/中和）と InChIKey による重複排除。\n\n"
            "> ステップ 4: 結果の解析\n"
            "結果タブで Ideal / All / Discard を切替。行をクリックすると 2D 構造と物性を表示します。\n"
            "🧩 'カスタム…' で表示列を選択（データが無くても設定可）。\n"
            "🧬 立体化学/キラリティ: Has_Stereo と不斉中心数（定義/未定義）を SMILES_Final から計算します。\n"
            "💾 表の下: CSV/XLSX/PDF の出力、SMILES コピー、候補を ADMET タブへ送る操作があります。\n"
            "🧠 ADMET タブは統合検索ワークスペースとして動作し、SMILES の貼り付け、Ideal 候補の読み込み、検索による候補移動、ローカル出力の確認をポップアップなしで行えます。\n"
            "🧪 ADMET の折りたたみパネルには、候補の読み込み方、予測の読み方、優先順位付けワークフローがまとめられています。\n"
            "🧩 3D ZIP と ADMET CSV は ADMET タブから実行し、すべての Ideal 候補または手動選択した候補群を出力できます。\n"
            "⚠️ ADMET 予測は初期スクリーニング向けの参考値であり、実験的証拠の代替ではありません。\n"
            "💬 右上のフィードバックで要望/不具合報告ができます。\n\n"
            "> ステップ 5: 3D ZIP の出力\n"
            "ADMET タブから、Ideal 候補全体または手動選択した候補群について、3D コンフォーマー（SDF）の ZIP または ADMET CSV を書き出せます。\n\n"
            "⚠️ トラブルシューティング\n"
            "• 有効な生成物がない: しきい値を下げる/SMILES を確認。\n"
            "• RDKit: `conda install -c conda-forge rdkit`。\n"
            "• .numbers: 必要に応じて .xlsx/.csv に変換。\n"
            "• パフォーマンス: 成分あたり 50,000 件以下推奨。\n\n"
            "- 下のボタンからテンプレートをダウンロードできます -\n"
        ),
        "guide_templates_title": "サンプルテンプレートをダウンロード:",
        "guide_template_csv": "CSV テンプレート (.csv)",
        "guide_template_txt": "TXT/TSV テンプレート (.txt)",
        "guide_template_xlsx": "Sheets テンプレート (.xlsx)",
        "guide_packs_title": "反応別パック (.zip):",
        "guide_pack_biginelli": "Biginelli パック",
        "guide_pack_gbb": "GBB パック",
        "guide_pack_gewald": "Gewald パック",
        "about_desc": "Biginelli / GBB / Gewald による 3 成分 MCR の仮想ライブラリ生成と、記述子・Drug-likeness ルール・InChIKey 重複・PAINS/Brenk アラートを用いた優先度付けを提供します。CSV/XLSX/PDF/3D ZIP を出力できます。",
    },
    "中文": {
        # Core navigation
        "titulo": "Moleku v1.1.0",
        "tab_motor": "引擎 {rxn}",
        "tab_resultados": "结果",
        "tab_guide": "指南",
        "tab_acerca": "关于",
        "feedback": "反馈",

        # Motor
        "info_formato": "ℹ 格式: .csv, .txt, .tsv, .xlsx, .xls, .ods, .json, .numbers  |  列: NAME 与 SMILES",
        "mcr_label": "MCR:",
        "data_preview": "数据预览",
        "csv_de": "{comp} 文件:",
        "examinar": "浏览…",
        "reactivos_centrales": "中心试剂:",
        "core_reagents_select_hint": "选择一个或多个",
        "core_reagents_selected": "已选择",
        "core_reagents_selected_none": "无",
        "core_reagents_tip": "选择多个试剂可在一次运行中生成所有组合。",
        "umbral": "分数阈值 (%):",
        "ideal_rule": "理想准则:",
        "standardize": "标准化产物（去盐/中和）",
        "iniciar": "▶  开始生成",
        "limpiar": "✕  清空列表",
        "procesando": "处理中…",
        "listo": "完成。",
        "error_archivos": "请加载所有文件。",
        "missing_libraries": "缺少库",
        "no_valid_products": "未生成有效产物。请检查 SMILES 或降低阈值。",

        # Results / exports
        "exportar_csv": "导出 CSV",
        "exportar_xlsx": "导出 XLSX",
        "exportar_pdf": "导出 PDF",
        "exportar_zip": "导出 3D ZIP",
        "no_datos": "无数据。",
        "saved": "已保存:",
        "registros": "条",
        "table_view_custom": "自定义…",
        "table_cols_title": "表格列",
        "table_cols_apply": "应用",
        "table_cols_cancel": "取消",
        "results_toggle_info_hide": "隐藏信息面板",
        "results_toggle_info_show": "显示信息面板",

        # ADMET web
        "admet_open_web": "打开 ADMET-IA（网页）",
        "admet_copy_sel": "复制 SMILES（选择）",
        "admet_copy_ideal": "复制 SMILES（Ideal）",
        "admet_no_selection": "请在表格中选择一行或多行。",
        "tab_admet": "ADMET",
        "admet_missing_pkg_app": "此可执行文件中的本地 ADMET 运行时不可用。\n\n请使用更新后的 Moleku 构建版本，或重新打包并包含完整的 ADMET 运行环境。",
        "admet_export_csv": "导出 ADMET（CSV）",
        "admet_tab_hint": "在此标签中粘贴一个或多个 SMILES，或直接从结果中导入 Ideal 候选，以搜索式工作流查看本地 ADMET 预测。",
        "admet_tab_input_title": "候选输入",
        "admet_tab_input_hint": "每行粘贴一个 SMILES，使用搜索栏查看已计算候选，或导入 Moleku 生成的 Ideal 候选。",
        "admet_info_title": "ADMET 快速说明",
        "admet_info_hint": "简要说明如何加载候选、理解输出，以及如何从 ADMET 导出有用的候选子集。",
        "admet_tab_run_input": "运行已粘贴的 SMILES",
        "admet_tab_use_ideal": "使用 Ideal 结果",
        "admet_tab_search": "搜索候选/SMILES:",
        "admet_tab_search_clear": "清除",
        "admet_tab_results_count": "已分析候选: {n} / {total}",
        "admet_tab_no_predictions": "尚无集成的 ADMET 预测。",
        "admet_tab_select_candidate": "搜索候选或运行预测，以查看其结构和 ADMET 输出。",
        "admet_tab_candidate_title_empty": "2D 查看器",
        "admet_tab_candidate_title": "当前查看: {candidate}",
        "admet_tab_candidate_smiles": "SMILES: {smiles}",
        "admet_tab_summary_title_empty": "已选 ADMET 输出",
        "admet_tab_summary_title": "已选 ADMET 输出 — {candidate}",
        "admet_tab_summary_empty": "所选候选的 ADMET 输出将显示在这里。",
        "admet_tab_no_input_smiles": "请在 ADMET 输入框中至少粘贴一个有效的 SMILES。",
        "admet_tab_no_ideal_results": "没有可发送到 ADMET 的 Ideal 候选。",
        "admet_tab_running": "正在为 {n} 个候选计算本地 ADMET...",
        "admet_help_input_title": "如何加载候选",
        "admet_help_input": (
            "• 可直接在右上输入框中逐行粘贴 SMILES。\n"
            "• 也支持以制表符、逗号或分号分隔的 名称/SMILES 对。\n"
            "• 以 '#' 开头的行会被当作注释忽略，重复的 SMILES 会在运行前去重。\n"
            "• 还可以直接从结果页导入 Ideal 候选。\n"
            "• 搜索栏只筛选已计算的候选，不会重新运行 ADMET。"
        ),
        "admet_help_outputs_title": "如何理解 ADMET 输出",
        "admet_help_outputs": (
            "• 2D 查看器显示当前激活候选的结构。\n"
            "• “已选 ADMET 输出”面板列出该候选的本地预测结果。\n"
            "• 当你搜索并切换候选时，查看器和输出面板会在同一标签内同步更新。\n"
            "• 这些值适合用于早期筛选优先级排序，但不能替代实验验证。\n"
            "• 常见预警包括极低渗透性、较高预测毒性，或相似候选之间出现矛盾的性质分布。"
        ),
        "admet_help_workflow_title": "建议的 ADMET 工作流",
        "admet_help_workflow": (
            "1) 在 Moleku 中生成候选，或粘贴外部 SMILES 批次。\n"
            "2) 在此标签中运行本地 ADMET。\n"
            "3) 使用顶部搜索栏在已计算候选之间快速切换。\n"
            "4) 对比 2D 结构与 ADMET 输出，排序最佳/最差的候选画像。\n"
            "5) 为所有 Ideal 候选或手动选择的候选子集导出 ADMET CSV 或 3D ZIP。\n"
            "6) 将最优候选保留用于更深入分析或外部验证。"
        ),
        "export_select_title_3d": "选择用于 3D ZIP 的候选",
        "export_select_title_admet": "选择用于 ADMET 导出的候选",
        "export_select_hint": "选择导出全部 Ideal 候选，或手动选择一部分特定候选。",
        "export_select_mode_ideal": "导出全部 Ideal 候选",
        "export_select_mode_manual": "手动选择特定候选",
        "export_select_candidates": "可用候选",
        "export_select_all": "全选",
        "export_select_clear": "清空选择",
        "export_select_apply": "导出",
        "export_select_cancel": "取消",
        "export_select_need_candidates": "没有可导出的候选。",
        "export_select_need_manual": "请至少选择一个候选进行导出。",

        # Chirality labels (panel keys)
        "stats_has_stereo": "立体化学",
        "stats_chiral_centers": "手性中心",

        # Info panels (Results)
        "results_help_params_title": "这些参数是什么意思？",
        "results_help_params": (
            "• 兼容性评分（%）: 由 LogP/MW/TPSA 计算的 0–100 指标（越高越好）。\n"
            "• MW: 分子量（Da）。\n"
            "• LogP: 脂溶性（RDKit 估计）。\n"
            "• TPSA: 拓扑极性表面积。\n"
            "• HBA/HBD: 氢键受体/供体。\n"
            "• 其他: 可旋转键、重原子数、环数、摩尔折射率等。\n"
            "• PAINS/Brenk: 结构警示（启发式）。\n"
            "• InChIKey: 用于重复检测。\n"
            "• 立体化学/手性:\n"
            "  - Has_Stereo: 产物 SMILES 含立体信息（@ 或 E/Z）则为 True。\n"
            "  - Chiral_Centers: RDKit 检测到的手性中心数量。\n"
            "  - Unassigned: 存在手性中心但未指定 R/S。\n"
            "\n"
            "分类（Ideal / Discard）\n"
            "- Ideal: 满足所选理想准则。\n"
            "- Discard: 不满足准则/阈值或生成失败。\n"
            "\n"
            "导出\n"
            "- 表格下方: CSV/XLSX/PDF/3D ZIP、复制 SMILES、打开 ADMET‑IA（网页/本地）。\n"
            "- 新增: CSV/XLSX/PDF 现在会遵循表格当前筛选（Ideal / All / Discard），导出的文件与可见行完全一致，不会出现空白单元格。建议的文件名包含筛选名称（例如 mcrg_results_ideal.csv）。\n"
            "- 3D ZIP 保持原有逻辑（始终仅导出 Ideal 化合物的 3D 构象），因为 3D 生成代价较高，专注于已优先的候选。\n"
            "- ADMET‑IA: '打开 ADMET-IA（网页）' 使用网页门户；'ADMET（本地）' 在安装可选包 'admet-ai' 时进行离线预测（pip install admet-ai）。\n"
            "- 高级功能将以 plugins/packs 形式逐步提供。\n"
        ),
        "results_help_workflow_title": "工作流程（概要）",
        "results_help_workflow": (
            "1) 选择反应与理想准则。\n"
            "2) 为每个组分加载 NAME/SMILES 文件。\n"
            "3) 生成组合（笛卡尔积）并用 RDKit SMARTS 执行反应。\n"
            "4) 可选：标准化。\n"
            "5) 计算描述符、评分、规则与警示。\n"
            "6) 计算 InChIKey 并标记重复。\n"
            "7) 进行 Ideal/Discard 分类。\n"
            "8) 结果筛选、列自定义、2D 预览。\n"
            "9) 导出 CSV/XLSX/PDF/3D ZIP。\n"
        ),
        "results_help_views_title": "如何理解 Ideal / All / Discard",
        "results_help_views": (
            "- Ideal: 满足理想准则的行。\n"
            "- Discard: 失败或不满足准则/阈值（可能仍保留 SMILES_Final 以便检查）。\n"
            "- All: 所有评估行。\n"
            "\n"
            "按筛选条件导出\n"
            "- CSV / Sheets (XLSX) / PDF 只导出当前视图（Ideal / All / Discard）；先筛选再导出可避免空白行。\n"
            "- 3D ZIP 不使用此筛选：始终只导出被分类为 Ideal 的化合物（3D 生成代价较高）。\n"
        ),

        # Guide/About
        "guide_title": "用户指南 — Moleku",
        "guide_text": (
            "欢迎使用 Moleku v1.1.0\n"
            "──────────────────────────────\n"
            "Moleku 是专业的桌面 CADD 平台，可通过多组分反应（MCR）快速生成虚拟文库。\n\n"
            "> 第 1 步：准备输入文件\n"
            "每个文件必须包含两列：NAME（标识符）与 SMILES（结构）。\n"
            "✅ 支持格式：.csv, .txt, .tsv, .dat, .smi, .xlsx, .xls, .ods, .json, .numbers\n"
            "🔍 分隔符自动识别：逗号/分号/制表符/空格/竖线。\n"
            "🧪 支持的 SMILES 形式包括 canonical、芳香小写写法、Kekule/非芳香表示、原子顺序不同但等价的写法、异构/立体化学形式（`@`, `/`, `\\`）以及与 RDKit 兼容的 CXSMILES。\n"
            "🗂 也支持单列 SMILES 文件，以及 SMILES、Canonical_SMILES、Isomeric_SMILES、CXSMILES 等常见列名。\n"
            "📄 示例：\n"
            "    NAME,SMILES\n"
            "    Benzaldehyde,c1ccccc1C=O\n"
            "    4-Nitrobenzaldehyde,O=Cc1ccc([N+](=O)[O-])cc1\n"
            "    Cinnamaldehyde_E,O=C/C=C/c1ccccc1\n\n"
            "> 第 2 步：选择 MCR 反应\n"
            "v1.1.0（core）仅包含三个三组分 MCR：Biginelli (3-CR)、GBB (3-CR)、Gewald (3-CR)。Ugi (4-CR) 等不在此版本范围。预览面板显示反应示意/DOI/说明。\n"
            "⚗️ 若反应包含中心试剂，可通过复选框生成组合变体。\n\n"
            "> 第 3 步：配置并运行\n"
            "为每个组分加载文件，设置分数阈值（0–100%），点击开始生成。\n"
            "⚙️ 引擎计算笛卡尔积并用 RDKit SMARTS 执行反应，再用评分与 Drug-likeness 规则进行评估。\n"
            "🧼 可选：标准化（去盐/中和）与基于 InChIKey 的去重。\n\n"
            "> 第 4 步：分析结果\n"
            "在结果页切换 Ideal / All / Discard；点击任意行查看 2D 结构与属性。\n"
            "🧩 “自定义…” 可选择显示列（即使没有数据也可预先设置）。\n"
            "🧬 立体化学/手性：从 SMILES_Final 计算 Has_Stereo 与手性中心数量（已定义/未指定）。\n"
            "💾 表格下方可导出 CSV/XLSX/PDF、复制 SMILES，并把候选发送到 ADMET 标签进行本地分析。\n"
            "🧠 ADMET 标签像一个集成搜索工作区：可粘贴 SMILES、导入 Ideal 候选、通过搜索栏切换化合物，并在同一界面查看本地输出，无需弹窗。\n"
            "🧪 ADMET 的折叠面板总结了候选加载方式、结果解读方法以及建议的优先级排序流程。\n"
            "🧩 3D ZIP 与 ADMET CSV 现在都从 ADMET 标签导出；既可导出全部 Ideal 候选，也可手动选择特定子集。\n"
            "⚠️ ADMET 预测用于早期筛选参考，不能替代实验验证。\n"
            "💬 右上角“反馈”用于建议与问题反馈。\n\n"
            "> 第 5 步：导出 3D ZIP\n"
            "可在 ADMET 标签中为全部 Ideal 候选或手动选择的候选子集导出 3D 构象 ZIP（SDF）或 ADMET CSV。\n\n"
            "⚠️ 排错与最佳实践\n"
            "• 无有效产物：降低阈值或检查 SMILES。\n"
            "• RDKit：`conda install -c conda-forge rdkit`。\n"
            "• .numbers：必要时导出为 .xlsx/.csv。\n"
            "• 性能建议：每个组分文件 < 50,000 行。\n\n"
            "- 使用下方按钮下载模板 -\n"
        ),
        "guide_templates_title": "下载示例模板:",
        "guide_template_csv": "CSV 模板 (.csv)",
        "guide_template_txt": "TXT/TSV 模板 (.txt)",
        "guide_template_xlsx": "Sheets 模板 (.xlsx)",
        "guide_packs_title": "反应现成包 (.zip):",
        "guide_pack_biginelli": "Biginelli 包",
        "guide_pack_gbb": "GBB 包",
        "guide_pack_gewald": "Gewald 包",
        "about_desc": "提供基于三组分 MCR（Biginelli、GBB、Gewald）的虚拟文库生成，并使用描述符、Drug-likeness 规则、InChIKey 去重与 PAINS/Brenk 警示进行优先级排序。支持导出 CSV/XLSX/PDF 与 3D ZIP。",
    },
}

# Ensure partial locales fall back to English for missing keys.
# This keeps the UI fully translated (no raw keys) while allowing incremental translation work.
_UPDATED_ENGLISH_FALLBACK_KEYS = (
    "admet_tab_hint",
    "admet_tab_input_hint",
    "admet_tab_use_results",
    "admet_tab_use_ideal",
    "admet_export",
    "admet_export_csv",
    "admet_export_title",
    "admet_export_hint",
    "admet_help_input",
    "admet_help_workflow",
    "admet_select_title_results",
    "admet_select_hint_results",
    "admet_select_mode_ideal",
    "admet_select_mode_generated",
    "admet_select_mode_manual",
    "export_table",
    "export_table_title",
    "export_table_hint",
    "export_scope",
    "export_format",
    "export_format_csv",
    "export_format_xlsx",
    "export_format_pdf",
    "export_scope_empty",
    "generated",
    "results_help_params",
    "results_help_workflow",
    "results_help_views_title",
    "results_help_views",
    "guide_text",
)
for _lang in ("Deutsch", "日本語", "中文"):
    try:
        if _lang in LOCALES and "English" in LOCALES:
            LOCALES[_lang] = {**LOCALES["English"], **LOCALES[_lang]}
            for _key in _UPDATED_ENGLISH_FALLBACK_KEYS:
                if _key in LOCALES["English"]:
                    LOCALES[_lang][_key] = LOCALES["English"][_key]
    except Exception:
        pass

try:
    _preferred_order = ("English", "Español", "Deutsch", "日本語", "中文")
    LOCALES = {
        **{_lang: LOCALES[_lang] for _lang in _preferred_order if _lang in LOCALES},
        **{_lang: data for _lang, data in LOCALES.items() if _lang not in _preferred_order},
    }
except Exception:
    pass
