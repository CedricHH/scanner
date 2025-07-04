import cv2
import numpy as np

def preprocess_image(image: np.ndarray) -> np.ndarray:
    """
    Führt Standard-Vorverarbeitungsschritte auf einem Bild aus.

    Args:
        image (np.ndarray): Das Eingabebild (BGR).

    Returns:
        np.ndarray: Das vorverarbeitete Schwarz-Weiß-Bild.
    """
    # 1. Konvertierung in Graustufen
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Binarisierung mit Otsu-Verfahren
    # Das Bild wird invertiert, damit der Text/die Markierungen weiß (255)
    # und der Hintergrund schwarz (0) ist. Das vereinfacht einige Analysen.
    _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Optional: Schräglagenkorrektur (Deskewing) - eine einfache Implementierung
    # Hinweis: Dies funktioniert gut für Dokumente mit klaren Textblöcken.
    # coords = np.column_stack(np.where(binary_image > 0))
    # angle = cv2.minAreaRect(coords)[-1]
    # if angle < -45:
    #     angle = -(90 + angle)
    # else:
    #     angle = -angle

    # (h, w) = image.shape[:2]
    # center = (w // 2, h // 2)
    # M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # # Verwende das binarisierte Bild für die Rotation, um Kantenartefakte zu minimieren
    # rotated = cv2.warpAffine(binary_image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    # return rotated

    return binary_image
