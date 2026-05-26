# Moleku (formerly MCR-G): Guía de Troubleshooting - "No se genera nada"
## 🔴 Problema: No se generan productos

Si ves el mensaje **"No Products Generated"** o la consola está vacía, sigue esta guía paso a paso.

---

## 1️⃣ **Verifica el Formato de los Archivos**

### ✅ CORRECTO: Archivo debe tener columnas NAME y SMILES

```
NAME,SMILES
Benzene,c1ccccc1
Toluene,Cc1ccccc1
Phenol,Oc1ccccc1
```

### ❌ INCORRECTO: Falta columna SMILES

```
NAME,IUPAC
Benzene,Benzeno
Toluene,Tolueno
```

**Archivos soportados:**
- ✅ CSV (comma-separated)
- ✅ TSV (tab-separated) 
- ✅ TXT (auto-detecta delimitador)
- ✅ XLSX/XLS (Excel)
- ✅ JSON
- ✅ NUMBERS (Apple)

---

## 2️⃣ **Valida que los SMILES sean correctos**

### ❌ SMILES inválidos se descartan automáticamente

```
BAD SMILES:
CCCC    ← válido (butano)
c1cccc  ← INVÁLIDO (anillo incompleto)
CC(C)C  ← válido (isobutano)
C#N#C   ← INVÁLIDO (enlace triple duplicado)
```

**Prueba tus SMILES:**
- Usa un generador online: https://www.smiles-explorer.com/
- O copia en Google: "SMILES string" + tu SMILES

---

## 3️⃣ **Revisa el Umbral (Threshold)**

**IMPORTANTE:** El umbral ahora es **0 por defecto** (aceptar todo)

- **Threshold = 0** → Acepta TODOS los productos ✅
- **Threshold = 50** → Solo 50% de calidad (muchos descartados)
- **Threshold = 100** → Solo perfecto (casi ninguno pasa)

**Si no ves resultados:**
1. Mueve el slider a **0** ← 
2. Haz clic en **"RUN"** de nuevo

---

## 4️⃣ **Verifica los Reactivos tengan Grupos Funcionales**

Cada reacción necesita ciertos grupos funcionales. Ejemplo:

### Reacción Biginelli (3-CR)
Necesita:
- ✅ **Aldehído** (CHO) → ejemplo: `O=Cc1ccccc1` (benzaldehído)
- ✅ **Beta-Cetoéster** (C(=O)OR) → ejemplo: `CC(=O)CC(=OOC)C` 
- ✅ **Urea** (NH2-C(=O)-NH2)

Si tus SMILES NO tienen estos grupos → **Cero productos**

---

## 5️⃣ **Lee el Mensaje de Error en la Consola**

La consola muestra información valiosa:

```
Example output:
— Aldehídos: 5 valid records —
— Beta-Cetoésteres: 3 valid records —
✅ 12 products | ❌ 1 failed | 📊 Total evaluated: 15
```

Si ves:
- `— Aldehídos: 0 valid records` → Archivo vacío o SMILES inválido
- `❌ 12 failed` → Problema con estructura de reacción
- `⚠ One or more files are empty` → Archivo no se cargó

---

## 🛠️ **Checklist Rápido**

- [ ] Archivos tienen columnas **NAME** y **SMILES**
- [ ] SMILES son válidos (probados en https://smiles-explorer.com)
- [ ] Reactivos tienen grupos funcionales para la reacción
- [ ] Threshold está en **0** (o valor bajo)
- [ ] Archivos NO están vacíos (>0 filas)
- [ ] Extensión correcta (.csv, .xlsx, .txt)

---

## 📧 Ejemplo de Archivo Correcto

```csv
NAME,SMILES
4-Fluorobenzaldehyde,O=Cc1ccc(F)cc1
3-Methoxybenzaldehyde,O=Cc1cc(OC)ccc1
2-Naphthaldehyde,O=Cc1ccc2ccccc2c1
Cinnamaldehyde,O=C/C=C/c1ccccc1
```

---

## 💡 Consejos

1. **Comienza con pocos archivos** (3-5 moléculas) para debug
2. **Usa SMILES canónicos** generados por RDKit
3. **Si sigue sin funcionar**, copia el mensaje de error completo de la consola
4. **Verifica el idioma** (English/Spanish) no afecta SMILES

---

## ¿Aún no funciona?

Ejecuta esto en terminal para debug avanzado:

```bash
cd /Users/pipelzm/Downloads/MCR-G
python -c "
from rdkit import Chem
smiles = 'O=Cc1ccccc1'  # Reemplaza con tu SMILES
mol = Chem.MolFromSmiles(smiles)
print(f'SMILES valid: {mol is not None}')
"
```

Si imprime `SMILES valid: True` → SMILES es correcto ✅
