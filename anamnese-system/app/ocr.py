import pytesseract
import numpy as np

# Optional: Setze den Pfad zur Tesseract-Installation, falls nicht im System-PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text(image: np.ndarray, coords: dict) -> str:
    """
    Extrahiert Text aus einem definierten Bildbereich.

    Args:
        image (np.ndarray): Das vorverarbeitete (binarisierte) Bild.
        coords (dict): Die Koordinaten des Textfeldes (x, y, width, height).

    Returns:
        str: Der extrahierte und bereinigte Text.
    """
    x, y, w, h = coords['x'], coords['y'], coords['width'], coords['height']

    # Schneide den Bereich des Textfeldes aus
    roi = image[y:y+h, x:x+w]

    if roi.size == 0:
        return ""

    # Konfigurationsoptionen für Tesseract
    # --psm 6: Gehe von einem einzelnen, einheitlichen Textblock aus.
    config = "--psm 6 -l deu"

    # Extrahiere Text mit Pytesseract
    text = pytesseract.image_to_string(roi, config=config)

    # Bereinige den Output
    return text.strip().replace('\n', ' ').replace('\f', '')
