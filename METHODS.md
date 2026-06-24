# Methods (Moleku — formerly Moleku)

This document describes the computational workflow implemented by Moleku for virtual library generation via multi-component reactions (MCRs), descriptor calculation, filtering, and reporting.

## 1) Inputs

Each component file contains two columns:
- `NAME`: identifier
- `SMILES`: reactant structure

Moleku loads the inputs, strips/cleans SMILES strings, and (when RDKit is available) filters out SMILES that RDKit cannot parse into molecules.

## 2) Library generation

For a selected reaction, Moleku enumerates combinations using the Cartesian product of the component lists (plus optional “core reagent” choices, when defined for that reaction).

For each combination it attempts to apply the reaction SMARTS (`RDKit AllChem.ReactionFromSmarts`) and records the attempt as either:
- a successful product (with `SMILES_Final`), or
- a discarded attempt with `Failure_Reason` describing the failure mode (invalid reactant, no products, sanitize failed, etc.).

## 3) Descriptor calculation

For successful products, Moleku computes common physicochemical descriptors (RDKit):
- Molecular weight (MW)
- LogP
- TPSA
- HBA / HBD

## 4) Filtering / classification

### Lipinski (Ro5)

The default “Ideal” classification is based on Lipinski’s Rule of Five thresholds:
- MW ≤ 500
- LogP ≤ 5
- HBD ≤ 5
- HBA ≤ 10

Products failing these limits keep their `SMILES_Final` and are marked with `Review_Status = Warning`, so they remain available for inspection and optional 3D export. Attempts that fail to produce a valid product are marked with `Review_Status = Error`.

### Additional rule-based filters

Moleku can label “Ideal” using other common drug-likeness heuristics (selectable in the UI), including:
- Ghose
- Veber
- Egan
- Muegge
- Any / All (aggregated across the above rules)

### Score threshold

Moleku also computes a simple compatibility score in the range 0–100 with penalties for deviating from target values (MW ≈ 350, LogP ≈ 2.5, TPSA ≈ 90). Results below the user threshold are marked as `Warning` with a “Below threshold” reason when they still have a valid `SMILES_Final`.

## 5) Standardization / uniqueness

Moleku can optionally standardize products before generating identifiers (toggle in the UI):
- RDKit cleanup
- fragment parent selection (desalting)
- uncharging (neutralization)

For products with a `SMILES_Final`, Moleku computes an `InChIKey` (when RDKit InChI is available) and flags duplicates:
- `Is_Duplicate`: whether this product repeats an earlier `InChIKey`
- `Duplicate_Of`: index of the first occurrence (for traceability)

The “Ideal” view suppresses duplicates by default to keep prioritization sets unique, while the “All” view preserves all evaluated attempts for auditing.

## 6) Reporting / exports

Moleku exports:
- CSV tables
- SDF (`results.sdf`) with properties embedded as SDF fields
- Publication-oriented plots (vector + raster)

### Reproducible Research Bundle

The Research Bundle ZIP includes:
- results (CSV + SDF)
- plots (and manifests)
- `run_manifest.json` recording parameters, environment versions, catalogue hash, and SHA256 hashes of input files (and best-effort copies of inputs in the bundle).
