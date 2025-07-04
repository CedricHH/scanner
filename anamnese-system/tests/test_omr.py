import numpy as np
from app.omr import is_checked

def test_is_checked_true():
    # Erzeuge ein Testbild (50x50), das zu 50% gefüllt ist (weiße Pixel)
    image = np.zeros((100, 100), dtype=np.uint8)
    image[25:75, 25:75] = 255  # Ein gefüllter Bereich

    coords = {'x': 25, 'y': 25, 'width': 50, 'height': 50}
    # Mit Threshold 0.2 sollte dies True sein (tatsächliche Ratio ist 1.0 im ROI)
    assert is_checked(image, coords, threshold=0.2) == True

def test_is_checked_false():
    # Erzeuge ein leeres Testbild
    image = np.zeros((100, 100), dtype=np.uint8)

    coords = {'x': 25, 'y': 25, 'width': 50, 'height': 50}
    # Sollte False sein, da keine weißen Pixel vorhanden sind
    assert is_checked(image, coords, threshold=0.2) == False
