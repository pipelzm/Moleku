# Moleku

## Project status

| Category | Status |
|---|---|
| **Documentation** | ![docs](https://img.shields.io/badge/docs-passing-brightgreen) |
| **CI** | ![ci](https://github.com/pipelzm/Moleku/actions/workflows/ci.yml/badge.svg) |
| **Builds** | ![release](https://img.shields.io/github/v/release/pipelzm/Moleku?include_prereleases=false) |
| **Dependencies** | ![rdkit](https://img.shields.io/badge/powered%20by-RDKit-4c8bf5) |
| **License** | ![license](https://img.shields.io/badge/license-Apache--2.0-blue) |

Moleku is a desktop platform for virtual library generation through multi-component reactions (MCRs), early-stage candidate prioritization, integrated local ADMET analysis, and export of research-ready datasets for medicinal chemistry and computational drug discovery workflows.

> The codebase keeps the historical `mcrg` package name and the `mcrg_desktop.py`
> entrypoint for backwards compatibility. The user-facing application and release
> assets are distributed under the **Moleku** name.

## Overview

Moleku combines reaction-based virtual enumeration with practical cheminformatics utilities in a single desktop application:

- reaction-driven library generation using curated MCR workflows
- physicochemical descriptor calculation and heuristic prioritization
- configurable Ideal/Discard classification rules
- duplicate detection through `InChIKey`
- integrated `ADMET` tab with local prediction workflow
- 2D structure inspection and searchable candidate review
- export to CSV, XLSX, PDF, ADMET CSV, and 3D ZIP conformer bundles

## Supported core workflows

`Moleku v1.0` currently focuses on three 3-component MCR workflows:

- `Biginelli (3-CR)`
- `GBB (3-CR)`
- `Gewald (3-CR)`

Each workflow can be combined with curated example templates and reaction-ready packs provided in the application.

## Main capabilities

### Virtual library generation

Moleku loads reagent files (`NAME`, `SMILES`), enumerates combinations, applies reaction SMARTS with RDKit, and records both successful products and discarded attempts with explicit failure reasons.

### Candidate prioritization

For generated products, Moleku computes common descriptors and supports heuristic classification through rules such as:

- `Lipinski`
- `Ghose`
- `Veber`
- `Egan`
- `Muegge`
- aggregated `Any / All` logic

### Integrated ADMET workspace

The `ADMET` tab is designed as an in-app search and review environment:

- paste one or more SMILES directly
- import Ideal candidates from generated results
- inspect local ADMET outputs without popup windows
- search previously computed candidates
- export all Ideal candidates or a selected subset

### Export workflows

Moleku can export:

- result tables (`CSV`, `XLSX`)
- report-ready `PDF`
- local `ADMET CSV`
- `3D ZIP` conformer bundles (`SDF`)

Additional methodological context is documented in `METHODS.md`.

## Installation and local development

Because RDKit packaging varies by operating system, the most reliable development setup is through `conda-forge`.

### Run from source

```bash
python mcrg_desktop.py
```

### Recommended development stack

```bash
mamba create -y -n moleku -c conda-forge python=3.11 rdkit pandas pillow numpy
mamba activate moleku
pip install customtkinter matplotlib openpyxl reportlab
```

For local ADMET predictions:

```bash
pip install admet-ai
```

## Desktop application builds

This repository includes a PyInstaller configuration in `mcrg.spec` and helper scripts for macOS packaging.

### Build locally

```bash
pyinstaller --clean --noconfirm mcrg.spec
```

For macOS app bundles:

```bash
bash scripts/build_mac_app.sh
```

Current packaged outputs include:

- `dist/Moleku.app` for Apple Silicon
- `dist/Moleku-macOS-x86_64.app` for Intel Macs
- `dist/Moleku-macOS.zip`
- `dist/Moleku-macOS-x86_64.zip`

## GitHub releases

For end users, the recommended distribution channel is the GitHub `Releases` section rather than committing binary app bundles into the repository history.

Recommended release assets:

- `Moleku-macOS.zip` for Apple Silicon
- `Moleku-macOS-x86_64.zip` for Intel Macs

## Repository structure

- `mcrg/` — application modules
- `examples/` — input templates and reaction-ready datasets
- `tests/` — automated regression coverage
- `scripts/` — packaging and helper scripts
- `packaging/` — distribution notes and platform-specific docs
- `METHODS.md` — computational workflow summary
- `QUICKSTART.md` — condensed startup guidance
- `TROUBLESHOOTING.md` — environment and runtime troubleshooting

## Documentation

Project-level documentation currently lives in the repository:

- `README.md` — project overview
- `METHODS.md` — computational methodology
- `QUICKSTART.md` — quick start guide
- `TROUBLESHOOTING.md` — setup and debugging guidance

## License

This project is distributed under the Apache License 2.0.

- full license text: `LICENSE`
- attribution and derivative-work notice: `NOTICE`

## Citation

If you use Moleku in academic work, please cite the software using the metadata provided in `CITATION.cff`.

## Author

**Felipe Lizama Mora**
