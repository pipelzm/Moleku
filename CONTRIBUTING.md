# Contributing to Moleku

Thank you for your interest in improving `Moleku`.

This project combines desktop application UX, cheminformatics workflows, and release engineering, so even small contributions can be valuable.

## Ways to contribute

- report bugs
- suggest new reactions or workflow improvements
- improve documentation
- add or refine tests
- improve packaging and distribution workflows
- submit code changes through pull requests

## Before opening an issue

Please include as much context as possible:

- operating system and architecture
- whether you are running from source or from a packaged app
- exact steps to reproduce
- expected behavior
- actual behavior
- screenshots or error messages when relevant

For chemistry-related issues, include a minimal example whenever possible:

- reaction selected
- input file format
- one or two representative `SMILES`
- observed output or `Failure_Reason`

## Development setup

The most reliable local environment uses `conda-forge` because of `RDKit`.

Example:

```bash
mamba create -y -n moleku -c conda-forge python=3.11 rdkit pandas pillow numpy
mamba activate moleku
pip install customtkinter matplotlib openpyxl reportlab
```

To run the desktop application locally:

```bash
python mcrg_desktop.py
```

Optional local ADMET support:

```bash
pip install admet-ai
```

## Code style expectations

- keep changes focused and easy to review
- preserve backwards compatibility when practical
- prefer clear, explicit code over clever shortcuts
- update user-facing copy when behavior changes
- avoid introducing large dependency changes unless justified

## Tests

If you modify logic that affects parsing, reaction execution, filtering, ADMET flow, or packaging behavior, add or update targeted tests when it meaningfully reduces regression risk.

Run the test suite with:

```bash
pytest
```

If a change affects packaged app behavior, include a short note about how you validated it.

## Pull requests

For pull requests, please summarize:

- what changed
- why it changed
- how you tested it
- any known limitations or follow-up work

Small, focused pull requests are preferred over large mixed changes.

## Security and sensitive data

Please do not commit:

- credentials
- private datasets
- generated app bundles
- local cache/build directories

Binary release artifacts should be attached to GitHub `Releases`, not committed into the repository history.
