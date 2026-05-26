from __future__ import annotations


def clean_smiles_text(value) -> str:
    if value is None:
        return ""
    try:
        if value != value:
            return ""
    except Exception:
        pass

    text = str(value).replace("\ufeff", "").strip()
    if len(text) >= 2 and text[0] == text[-1] and text[0] in ("'", '"'):
        text = text[1:-1].strip()
    return text


def smiles_candidates(value) -> list[str]:
    text = clean_smiles_text(value)
    if not text or text.lower() in {"nan", "none", "null"}:
        return []

    candidates = [text]
    if any(ch.isspace() for ch in text):
        first_token = text.split()[0].strip()
        if first_token and first_token not in candidates:
            candidates.append(first_token)
    return candidates


def _build_parser_params(Chem, *, sanitize: bool, parse_name: bool):
    try:
        params = Chem.SmilesParserParams()
    except Exception:
        return None

    for attr, value in (
        ("sanitize", bool(sanitize)),
        ("allowCXSMILES", True),
        ("strictCXSMILES", False),
        ("parseName", bool(parse_name)),
    ):
        if hasattr(params, attr):
            try:
                setattr(params, attr, value)
            except Exception:
                continue
    return params


def _mol_from_smiles(Chem, smiles: str, *, sanitize: bool, parse_name: bool):
    params = _build_parser_params(Chem, sanitize=sanitize, parse_name=parse_name)
    try:
        if params is not None:
            return Chem.MolFromSmiles(smiles, params)
        if sanitize:
            return Chem.MolFromSmiles(smiles)
        return Chem.MolFromSmiles(smiles, sanitize=False)
    except Exception:
        return None


def parse_smiles_flexible(value, Chem, *, sanitize: bool = True):
    if Chem is None:
        return None

    for candidate in smiles_candidates(value):
        for parse_name in (False, True):
            mol = _mol_from_smiles(Chem, candidate, sanitize=sanitize, parse_name=parse_name)
            if mol is not None:
                return mol

        raw = None
        for parse_name in (False, True):
            raw = _mol_from_smiles(Chem, candidate, sanitize=False, parse_name=parse_name)
            if raw is not None:
                break
        if raw is None:
            continue
        if not sanitize:
            return raw
        try:
            Chem.SanitizeMol(raw)
            return raw
        except Exception:
            continue
    return None


def is_valid_smiles_flexible(value, Chem) -> bool:
    return parse_smiles_flexible(value, Chem, sanitize=True) is not None


def canonicalize_smiles(value, Chem, *, isomeric: bool = True) -> str:
    mol = parse_smiles_flexible(value, Chem, sanitize=True)
    if mol is None:
        return ""
    try:
        return Chem.MolToSmiles(mol, canonical=True, isomericSmiles=bool(isomeric))
    except Exception:
        return ""
