# Plantillas de ejemplo — Moleku v1.0

Datasets mínimos (NAME, SMILES) listos para probar las **3 reacciones** del core v1.0.
Todas las plantillas son compatibles con cualquier formato soportado (CSV / TXT / TSV / XLSX / etc.); aquí van como CSV.

Estas plantillas mezclan varios estilos de escritura SMILES que Moleku acepta en el cargador:
- SMILES canónico
- aromático en minúsculas
- variantes equivalentes con distinto orden atómico
- formas estereoquímicas/isoméricas (`@`, `/`, `\`)
- notación cargada cuando corresponde (por ejemplo isocianuros)

## Mapeo plantilla → componente

| Archivo                  | Componente Moleku             | Reacciones donde se usa     |
|--------------------------|-------------------------------|------------------------------|
| `aldehydes.csv`          | Aldehídos                      | Biginelli, GBB              |
| `beta_ketoesters.csv`    | β-Cetoésteres                  | Biginelli                   |
| `isocyanides.csv`        | Isocianuros                    | GBB                         |
| `aminoazines.csv`        | 2-Aminoazinas                  | GBB                         |
| `ketones.csv`            | Cetonas                        | Gewald                      |
| `cyanoesters.csv`        | α-Cianoésteres                 | Gewald                      |

> Para **Biginelli** también necesitas elegir un reactivo central (Urea / Tiourea / Guanidina), pero eso se selecciona con checkboxes dentro de la app — no requiere archivo.
> Para **Gewald** el reactivo central es S₈ (azufre), también vía checkbox.

## Recetas rápidas

### Biginelli (3-CR)
1. **Aldehídos** → `aldehydes.csv`
2. **β-Cetoésteres** → `beta_ketoesters.csv`
3. **Reactivo central** → marca **Urea** (o las tres opciones para barrer todas las combinaciones).

### GBB (3-CR)
1. **Aldehídos** → `aldehydes.csv`
2. **Isocianuros** → `isocyanides.csv`
3. **2-Aminoazinas** → `aminoazines.csv`

### Gewald (3-CR)
1. **Cetonas** → `ketones.csv`
2. **α-Cianoésteres** → `cyanoesters.csv`
3. **Reactivo central** → **Azufre (S₈)** (viene marcado por defecto).

Ajusta el `Score threshold` y la **Ideal criterion** (Lipinski por defecto). Click en **▶ Start virtual generation**.

## Cobertura esperada con los packs oficiales

Referencia validada con los CSV de esta carpeta, `Score threshold = 0.0` e `Ideal criterion = Lipinski`.

| Reacción | Archivos / core | Intentos evaluados | Ideal esperados | Lectura rápida |
|----------|------------------|-------------------:|----------------:|----------------|
| Biginelli | `aldehydes.csv` + `beta_ketoesters.csv` + Urea | 63 | 63 | Pack completamente compatible |
| GBB | `aldehydes.csv` + `isocyanides.csv` + `aminoazines.csv` | 504 | 231 | Algunas aminoazinas quedan fuera del patrón GBB soportado |
| Gewald | `ketones.csv` + `cyanoesters.csv` + Azufre (S8) | 54 | 45 | Algunos pares generan productos no sanitizables |

Si una corrida oficial entrega `0 Ideal`, revisa primero que el umbral esté en `0.0`, que los archivos correspondan a la reacción elegida y que el reactivo central esté seleccionado cuando aplique.
