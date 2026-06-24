# Moleku v1.1.0 — Quick Start (Linux)

> Versión condensada. Para detalles, ver `INSTALL_LINUX.md` dentro del paquete.

## 1. Descomprimir
```bash
tar -xzf Moleku-Linux-source.tar.gz
cd Moleku-Linux-source
```

## 2. Instalar dependencias (una sola vez)

### Opción A — conda-forge (recomendada)
```bash
# Si no tienes mamba/conda: https://github.com/conda-forge/miniforge/releases/latest

mamba create -y -n moleku -c conda-forge python=3.11 rdkit pandas pillow numpy openpyxl reportlab
mamba activate moleku
pip install customtkinter matplotlib
# Opcional (predicciones ADMET locales):
pip install admet-ai
```

### Opción B — pip puro
```bash
python3.11 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install rdkit pandas pillow numpy customtkinter matplotlib openpyxl reportlab
```

## 3. Lanzar
```bash
./run_moleku.sh
# (equivalente: python mcrg_desktop.py)
```

## 4. Probar de inmediato
La carpeta `examples/` trae plantillas `NAME,SMILES` para las 3 reacciones:

| Reacción      | Carga estos archivos                                              |
|---------------|-------------------------------------------------------------------|
| **Biginelli** | `examples/aldehydes.csv` + `examples/beta_ketoesters.csv` + checkbox Urea |
| **GBB**       | `examples/aldehydes.csv` + `examples/isocyanides.csv` + `examples/aminoazines.csv` |
| **Gewald**    | `examples/ketones.csv` + `examples/cyanoesters.csv` + checkbox S₈ |

Las plantillas ahora incluyen ejemplos de SMILES en estilos distintos (canónico, aromático, orden alternativo, E/Z y notación cargada cuando aplica) para reflejar mejor la compatibilidad real del cargador.

Click en **▶ Start virtual generation** y luego ve a la pestaña **Results**.

## 5. Tips
- **Filtros y export**: la tabla separa `Ideal`, `Warning`, `Error`, `Generated` y `All`. `Warning` significa que existe `SMILES_Final`, pero no paso el criterio/umbral seleccionado.
- **3D ZIP** permite exportar `Ideal` o `Ideal + Warning` (todas las filas con `SMILES_Final`), bajo criterio del usuario.
- **ADMET (local)** requiere `pip install admet-ai`; sin él, usa **Abrir ADMET-IA (web)**.
