import cv2
import numpy as np

def is_checked(image: np.ndarray, coords: dict, threshold: float = 0.2) -> bool:
    """
    Prüft, ob ein Kästchen markiert ist, basierend auf dem Anteil nicht-schwarzer Pixel.

    Args:
        image (np.ndarray): Das vorverarbeitete (binarisierte, invertierte) Bild.
        coords (dict): Die Koordinaten des Kästchens (x, y, width, height).
        threshold (float): Der Schwellenwert (0.0 bis 1.0) für die Erkennung.

    Returns:
        bool: True, wenn das Kästchen als markiert erkannt wird.
    """
    x, y, w, h = coords['x'], coords['y'], coords['width'], coords['height']

    # Schneide den Bereich des Kästchens aus
    roi = image[y:y+h, x:x+w]

    if roi.size == 0:
        return False

    # Zähle die weißen Pixel (Markierungen auf dem invertierten Bild)
    filled_pixels = cv2.countNonZero(roi)

    # Berechne den prozentualen Anteil
    total_pixels = roi.shape[0] * roi.shape[1]
    ratio = filled_pixels / total_pixels

    return ratio > threshold
