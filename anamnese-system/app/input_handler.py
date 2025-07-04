import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image
import io

def load_form_as_image(file_path: str, page_number: int = 0, dpi: int = 300) -> np.ndarray:
    """
    Lädt eine Datei (PDF oder Bild) und konvertiert sie in ein OpenCV-kompatibles Bild.

    Args:
        file_path (str): Der Pfad zur Eingabedatei.
        page_number (int): Die zu verarbeitende Seite bei einer PDF-Datei.
        dpi (int): Die Auflösung für die PDF-zu-Bild-Konvertierung.

    Returns:
        np.ndarray: Das Bild als NumPy-Array im BGR-Format.
    """
    file_extension = file_path.split('.')[-1].lower()

    if file_extension == 'pdf':
        # Öffne das PDF-Dokument
        doc = fitz.open(file_path)
        if page_number >= len(doc):
            raise ValueError(f"Ungültige Seitenzahl: {page_number}. PDF hat nur {len(doc)} Seiten.")

        page = doc.load_page(page_number)

        # Rendere die Seite als Bild
        pix = page.get_pixmap(dpi=dpi)
        img_bytes = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_bytes))

        # Konvertiere von RGB (Pillow-Standard) zu BGR (OpenCV-Standard)
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    elif file_extension in ['png', 'jpg', 'jpeg', 'tiff']:
        # Lade die Bilddatei direkt
        image = cv2.imread(file_path)
        if image is None:
            raise FileNotFoundError(f"Bilddatei konnte nicht unter {file_path} gefunden oder gelesen werden.")
        return image

    else:
        raise ValueError(f"Nicht unterstützter Dateityp: {file_extension}")
