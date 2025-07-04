import json

def load_template(path: str) -> dict:
    """
    Lädt die JSON-Template-Datei.

    Args:
        path (str): Der Pfad zur JSON-Datei.

    Returns:
        dict: Das geladene Template als Dictionary.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Template-Datei nicht gefunden unter: {path}")
    except json.JSONDecodeError:
        raise ValueError(f"Fehler beim Parsen der JSON-Datei: {path}")
