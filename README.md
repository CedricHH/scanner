# scanner
Ziel der Entwicklung

Das Ziel ist die Entwicklung eines robusten, modularen Systems zur automatisierten Datenerfassung aus Anamnesebögen. Das System soll in der Lage sein, sowohl digital ausgefüllte PDF-Dateien als auch eingescannte, handschriftlich ausgefüllte Formulare (als Bilddateien wie PNG, JPG) zu verarbeiten. Das Endergebnis ist ein strukturiertes JSON-Objekt, das alle erfassten Informationen enthält und eine nahtlose Weiterverarbeitung in nachgelagerten Systemen ermöglicht.

Strukturierter Implementierungsplan für die Codebase

Dieser Plan priorisiert modulare Entwicklung und Testbarkeit. Jede Komponente wird als eigenständiger Baustein entwickelt, bevor sie in das Gesamtsystem integriert wird.

Schritt 1: Projekt-Setup und Abhängigkeiten

Die Basis für den gesamten Code.

* Aktion: Erstellen der Projektstruktur und Konfiguration der Entwicklungsumgebung.

* Implementierungsdetails:

* Anlegen des Hauptprojektverzeichnisses.

* Einrichten einer virtuellen Umgebung (z.B. venv oder conda).

* Installation der Kernbibliotheken:

* PyMuPDF oder pdf2image: Zur Umwandlung von PDF in Bilder.

* OpenCV-Python (cv2): Für sämtliche Bildverarbeitungsaufgaben.

* Pillow: Als Helferbibliothek für die Bildmanipulation.

* pytesseract: Als Schnittstelle zur Tesseract OCR-Engine.

Schritt 2: Modul zur Input-Verarbeitung (Input-Handler)

Ein dediziertes Modul, das verschiedene Eingabeformate verarbeiten und in ein einheitliches Format für die weitere Verarbeitung umwandeln kann.

* Aktion: Entwicklung einer Funktion, die einen Dateipfad entgegennimmt, den Dateityp (PDF, PNG, JPG etc.) erkennt und eine standardisierte Bildrepräsentation zurückgibt.

* Implementierungsdetails:

* Eine Funktion load_form_as_image(file_path: str, page_number: int = 0, dpi: int = 300).

* Logik:

* Wenn die Dateiendung .pdf ist, wird die angegebene Seite mit PyMuPDF oder pdf2image in ein Bild (NumPy-Array) konvertiert.

* Wenn die Dateiendung .png, .jpg, .jpeg oder .tiff ist, wird die Datei direkt mit cv2.imread() geladen.

* Der Rückgabewert ist immer ein für OpenCV verarbeitbares Bild im NumPy-Array-Format.

Schritt 3: Modul zur Bildvorverarbeitung (Preprocessor)

Ein universelles Modul zur Optimierung der Bilder für die Analyse.

* Aktion: Entwicklung einer Reihe von Funktionen zur Bildverbesserung.

* Implementierungsdetails:

* Funktion preprocess_image(image):

* Konvertierung in Graustufen.

* Binarisierung: Umwandlung in ein reines Schwarz-Weiß-Bild (z.B. mittels Otsu-Schwellenwertverfahren), um Störungen zu minimieren.

* Schräglagenkorrektur (Deskewing): Automatische Begradigung des Bildes.

Schritt 4: Template-Definition und Lader

Das Gehirn des Systems, das die Formularstruktur definiert. Dies ist keine Code-Implementierung, sondern die Erstellung einer Konfigurationsdatei.

* Aktion: Erstellen einer form_template.json-Datei, die alle Felder des Formulars mit Typ und Koordinaten abbildet.

* Implementierungsdetails:

* Die JSON-Datei enthält für jede Seite eine Liste von Feldern.

* Jedes Feld hat folgende Attribute:

* id: Ein eindeutiger Bezeichner (z.B. "herzschrittmacher").

* label: Die Frage auf dem Formular (z.B. "Herzschrittmacher?").

* type: Der Feldtyp (omr oder ocr).

* coords: Ein Objekt mit den Pixelkoordinaten (x, y, width, height) des Feldes. Bei omr enthält es die Koordinaten für die "Ja"- und "Nein"-Boxen.

* Erstellung einer einfachen Python-Funktion load_template(path), die diese JSON-Datei lädt und als Dictionary zurückgibt.

Schritt 5: Kernlogik-Modul: Optical Mark Recognition (OMR)

Ein spezialisiertes Modul zur Erkennung von Markierungen.

* Aktion: Entwicklung einer Funktion, die prüft, ob ein Kontrollkästchen markiert ist.

* Implementierungsdetails:

* Funktion is_checked(image, coords: dict) -> bool.

* Die Funktion schneidet den Bildbereich anhand der übergebenen coords zu.

* Sie berechnet den Anteil der schwarzen Pixel im zugeschnittenen Bereich.

* Ist der Anteil höher als ein definierter Schwellenwert (z.B. 20 %), gibt die Funktion True zurück, andernfalls False.

Schritt 6: Kernlogik-Modul: Optical Character Recognition (OCR)

Ein spezialisiertes Modul zur Texterkennung.

* Aktion: Entwicklung einer Funktion, die Text aus einem Bildbereich extrahiert.

* Implementierungsdetails:

* Funktion extract_text(image, coords: dict) -> str.

* Die Funktion schneidet den Bildbereich anhand der coords zu.

* Sie übergibt den Bildausschnitt an pytesseract.image_to_string() mit der Sprachoption für Deutsch (lang='deu').

* Der erkannte Text wird bereinigt (z.B. Entfernung von Steuerzeichen) und zurückgegeben.

Schritt 7: Orchestrierungs-Engine

Das Herzstück der Anwendung, das alle Module miteinander verbindet und den gesamten Prozess steuert.

* Aktion: Entwicklung einer Hauptklasse oder eines Hauptskripts, das den gesamten Workflow von Anfang bis Ende ausführt.

* Implementierungsdetails:

* Nimmt einen Dateipfad als Input.

* Lädt das Template (Schritt 4).

* Iteriert durch die Seiten des Formulars (1-4).

* Für jede Seite:

* Lädt die Seite als Bild (Schritt 2).

* Wendet die Bildvorverarbeitung an (Schritt 3).

* Iteriert durch alle im Template definierten Felder für diese Seite.

* Ruft je nach Feld-type die OMR- (Schritt 5) oder OCR-Funktion (Schritt 6) mit den entsprechenden Koordinaten auf.

* Speichert das Ergebnis (z.B. {"herzschrittmacher": True}) in einem Ergebnis-Dictionary.

* Gibt das vollständig befüllte Ergebnis-Dictionary als strukturiertes JSON zurück.

Schritt 8: Test-Framework

Implementierung von Tests zur Sicherstellung der Codequalität und Genauigkeit.

* Aktion: Einrichten von Unit- und Integrationstests mit pytest.

* Implementierungsdetails:

* Unit-Tests: Separate Tests für das OMR-Modul (mit Beispielbildern von leeren und angekreuzten Kästchen) und das OCR-Modul (mit Beispielbildern von Textfeldern).

* Integrationstest: Ein Test, der ein komplett ausgefülltes Beispiel-PDF und eine Beispiel-Bilddatei durch die gesamte Orchestrierungs-Engine (Schritt 7) laufen lässt und das resultierende JSON mit einer vorab erstellten "Ground-Truth"-JSON-Datei vergleicht.

Schritt 9: Anwendungs-Interface (API/CLI)

Die finale Schicht, die die Interaktion mit dem System ermöglicht.

* Aktion: Entwicklung einer Schnittstelle, um die Funktionalität für den Endnutzer zugänglich zu machen.

* Implementierungsdetails:

* Option A (CLI): Verwendung von argparse oder Click, um ein Kommandozeilen-Tool zu erstellen, das den Dateipfad als Argument entgegennimmt und den JSON-Output in die Konsole oder eine Datei schreibt.

* Option B (Web-API): Verwendung von FastAPI oder Flask, um einen API-Endpunkt (/process) zu erstellen, der eine Datei per Upload entgegennimmt und die erkannten Daten als JSON-Antwort zurückgibt.
