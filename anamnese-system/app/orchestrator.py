from app.input_handler import load_form_as_image
from app.preprocessor import preprocess_image
from app.template_loader import load_template
from app.omr import is_checked
from app.ocr import extract_text

def process_form(file_path: str, template_path: str) -> dict:
    """
    Orchestriert den gesamten Prozess der Datenextraktion aus einem Formular.

    Args:
        file_path (str): Pfad zur PDF- oder Bilddatei.
        template_path (str): Pfad zur JSON-Template-Datei.

    Returns:
        dict: Ein Dictionary mit den extrahierten Daten.
    """
    # 1. Lade das Template
    template = load_template(template_path)

    results = {"form_name": template.get("form_name", "Unknown Form"), "data": {}}

    # 2. Iteriere durch die Seiten des Templates
    for page_template in template.get("pages", []):
        page_num = page_template.get("page_number")

        try:
            # 3. Lade die Seite als Bild
            image = load_form_as_image(file_path, page_number=page_num)

            # 4. Wende die Bildvorverarbeitung an
            processed_image = preprocess_image(image)

            # 5. Iteriere durch die Felder der Seite
            for field in page_template.get("fields", []):
                field_id = field["id"]
                field_type = field["type"]
                coords = field["coords"]

                if field_type == "ocr":
                    # Rufe OCR-Funktion auf
                    text_result = extract_text(processed_image, coords)
                    results["data"][field_id] = text_result

                elif field_type == "omr":
                    # Rufe OMR-Funktion für "Ja" und "Nein" auf
                    ja_checked = is_checked(processed_image, coords["ja"])
                    nein_checked = is_checked(processed_image, coords["nein"])

                    # Logik zur Auswertung des OMR-Ergebnisses
                    if ja_checked and not nein_checked:
                        results["data"][field_id] = "Ja"
                    elif nein_checked and not ja_checked:
                        results["data"][field_id] = "Nein"
                    else:
                        # Fall: beide oder keines angekreuzt -> unklares Ergebnis
                        results["data"][field_id] = "Unklar"

        except (ValueError, FileNotFoundError) as e:
            print(f"Fehler bei der Verarbeitung von Seite {page_num}: {e}")
            continue # Springe zur nächsten Seite

    return results
