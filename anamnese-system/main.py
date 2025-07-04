import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.orchestrator import process_form

# Temporäres Verzeichnis für Uploads
TEMP_DIR = "temp_uploads"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Pfad zur Template-Datei
TEMPLATE_PATH = "form_template.json"

app = FastAPI(
    title="Anamnesebogen Auslese-API",
    description="Diese API extrahiert Daten aus hochgeladenen Anamnesebögen (PDF oder Bild).",
    version="1.0.0"
)

@app.post("/process", summary="Anamnesebogen verarbeiten")
async def process_uploaded_form(file: UploadFile = File(...)):
    """
    Nimmt eine Formular-Datei entgegen, speichert sie temporär,
    verarbeitet sie und gibt die extrahierten Daten als JSON zurück.
    """
    # Ensure TEMP_DIR exists, in case it was deleted or not created at startup
    if not os.path.exists(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR)
        except OSError as e:
            # Handle potential race condition or permission issues if directory creation fails
            raise HTTPException(status_code=500, detail=f"Konnte temporäres Upload-Verzeichnis nicht erstellen: {str(e)}")


    temp_file_path = os.path.join(TEMP_DIR, file.filename)

    try:
        # Speichere die hochgeladene Datei temporär
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Überprüfe, ob die Template-Datei existiert
        if not os.path.exists(TEMPLATE_PATH):
            raise HTTPException(status_code=500, detail="Server-Konfigurationsfehler: Template nicht gefunden.")

        # Rufe die Orchestrierungs-Engine auf
        extracted_data = process_form(temp_file_path, TEMPLATE_PATH)

        return extracted_data

    except HTTPException as http_exc: # Re-raise HTTPException
        raise http_exc
    except FileNotFoundError as fnf_error:
        # Specific error for file not found during processing (e.g. template moved after check)
        raise HTTPException(status_code=500, detail=f"Datei nicht gefunden während der Verarbeitung: {str(fnf_error)}")
    except ValueError as val_error:
        # Specific error for value errors during processing (e.g., invalid PDF page)
        raise HTTPException(status_code=400, detail=f"Ungültige Eingabe oder Daten: {str(val_error)}")
    except Exception as e:
        # Gib einen aussagekräftigen Fehler zurück für andere unerwartete Fehler
        # Loggen Sie den Fehler hier idealerweise auch serverseitig
        print(f"Unerwarteter Fehler in process_uploaded_form: {type(e).__name__} - {str(e)}") # Basic logging
        raise HTTPException(status_code=500, detail=f"Ein interner Serverfehler ist aufgetreten: {str(e)}")

    finally:
        # Lösche die temporäre Datei nach der Verarbeitung
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
            except OSError as e:
                # Log error if removal fails, but don't let it crash the response
                print(f"Fehler beim Löschen der temporären Datei {temp_file_path}: {str(e)}")


@app.get("/", summary="API Status")
def read_root():
    return {"status": "API läuft", "message": "Willkommen bei der Anamnesebogen Auslese-API!"}

# Optional: Add a cleanup for TEMP_DIR on shutdown, though this is often handled by deployment environments
# from fastapi import FastAPI, APIRouter
#
# @app.on_event("shutdown")
# def shutdown_event():
#     if os.path.exists(TEMP_DIR):
#         try:
#             shutil.rmtree(TEMP_DIR)
#             print(f"Temporäres Verzeichnis {TEMP_DIR} bei Shutdown gelöscht.")
#         except OSError as e:
#             print(f"Fehler beim Löschen des temporären Verzeichnisses {TEMP_DIR} bei Shutdown: {e}")
#     pass
