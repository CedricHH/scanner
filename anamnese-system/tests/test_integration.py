# This file is for integration tests.
# TODO: Add actual integration tests for the application.

import pytest
import os
import json
from fastapi.testclient import TestClient
from app.main import app # Assuming your FastAPI app instance is named 'app' in main.py

# It's good practice to use a TestClient for FastAPI integration tests
client = TestClient(app)

# Define a temporary directory for test uploads and a sample template path
TEST_TEMP_DIR = "temp_test_uploads"
# You'll need a sample form_template.json for testing.
# For now, let's assume it's the one in the root or create a specific one for tests.
SAMPLE_TEMPLATE_PATH = "form_template.json" # Adjust if needed or create a test-specific template

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    # Create a dummy template if it doesn't exist, or ensure the main one is used
    if not os.path.exists(SAMPLE_TEMPLATE_PATH):
        # Create a minimal valid template for testing basic API functionality
        dummy_template_content = {
            "form_name": "Test Anamnesebogen",
            "pages": [{
                "page_number": 0,
                "fields": [{
                    "id": "test_field", "label": "Test Field", "type": "ocr",
                    "coords": {"x": 10, "y": 10, "width": 100, "height": 20}
                }]
            }]
        }
        with open(SAMPLE_TEMPLATE_PATH, "w") as f:
            json.dump(dummy_template_content, f)
        created_template = True
    else:
        created_template = False

    # Create temp directory for uploads if it doesn't exist
    if not os.path.exists(TEST_TEMP_DIR):
        os.makedirs(TEST_TEMP_DIR)

    yield # This is where the testing happens

    # Teardown: Clean up created files and directories
    if os.path.exists(TEST_TEMP_DIR):
        for item in os.listdir(TEST_TEMP_DIR):
            os.remove(os.path.join(TEST_TEMP_DIR, item))
        os.rmdir(TEST_TEMP_DIR)

    if created_template and os.path.exists(SAMPLE_TEMPLATE_PATH):
        # Only remove if this fixture created it
        # Be careful if SAMPLE_TEMPLATE_PATH points to your main template
        # os.remove(SAMPLE_TEMPLATE_PATH) # Potentially dangerous if not handled well
        pass


def test_read_root_status():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API läuft", "message": "Willkommen bei der Anamnesebogen Auslese-API!"}

# To test the /process endpoint, you would need:
# 1. A sample PDF or image file.
# 2. Mocking for the functions within `process_form` (like load_form_as_image, preprocess_image, etc.)
#    OR a fully functional Tesseract and PyMuPDF setup in the test environment,
#    along with a file that can be processed.
#
# The latter is a true end-to-end test and can be complex to set up reliably in all environments.
# Mocking allows testing the API layer and orchestration logic more isolatedly.

# Example of a placeholder test for the process endpoint (would require a file)
# def test_process_form_valid_file():
#     # Create a dummy PDF/image file for upload
#     # For simplicity, let's assume we have a 'sample_form.pdf' in a test_data directory
#     # This part is highly dependent on your test data strategy
#
#     # Check if the main template exists, otherwise skip or fail gracefully
#     if not os.path.exists("form_template.json"):
#          pytest.skip("Main form_template.json not found, skipping integration test for /process")
#
#     # Create a dummy file to upload
#     dummy_file_path = os.path.join(TEST_TEMP_DIR, "dummy_form.txt") # Use .txt for simplicity, real test needs PDF/image
#     with open(dummy_file_path, "w") as f:
#         f.write("This is a dummy file.")
#
#     with open(dummy_file_path, "rb") as f_upload:
#         response = client.post("/process", files={"file": ("dummy_form.txt", f_upload, "text/plain")})
#
#     # Expected behavior depends on how robust process_form is to non-PDF/image files
#     # and whether Tesseract/PyMuPDF are fully mocked or operational.
#     # If it tries to process a .txt as PDF/image, it should ideally raise a specific error.
#
#     # This assertion will likely fail without proper mocking or a real processable file.
#     # assert response.status_code == 200
#     # assert "data" in response.json()
#
#     # For now, let's just check if the endpoint runs and returns some JSON,
#     # which might be an error JSON if the file is invalid.
#     assert response.headers["content-type"] == "application/json"
#     if response.status_code == 500:
#         # This is expected if a .txt file is sent and the input_handler fails
#         assert "Ein Fehler ist aufgetreten" in response.json()["detail"]
#     elif response.status_code == 200:
#         # This would only happen if the dummy file somehow got processed
#         assert "data" in response.json()
#     else:
#         pytest.fail(f"Unexpected status code: {response.status_code}, response: {response.text}")
#
#     if os.path.exists(dummy_file_path):
#         os.remove(dummy_file_path)

# def test_process_form_missing_template():
#     # Temporarily rename the template to simulate it missing
#     original_template_path = "form_template.json"
#     temp_missing_template_path = "form_template.json.bak"
#
#     if os.path.exists(original_template_path):
#         os.rename(original_template_path, temp_missing_template_path)
#
#     dummy_file_path = os.path.join(TEST_TEMP_DIR, "dummy_file_for_missing_template_test.txt")
#     with open(dummy_file_path, "w") as f:
#         f.write("content")
#
#     with open(dummy_file_path, "rb") as f_upload:
#         response = client.post("/process", files={"file": ("test.txt", f_upload, "text/plain")})
#
#     assert response.status_code == 500
#     assert "Server-Konfigurationsfehler: Template nicht gefunden." in response.json()["detail"]
#
#     # Restore the template
#     if os.path.exists(temp_missing_template_path):
#         os.rename(temp_missing_template_path, original_template_path)
#     if os.path.exists(dummy_file_path):
#         os.remove(dummy_file_path)


print("Basic test_integration.py created. More comprehensive integration tests are needed, especially for the /process endpoint with actual file uploads and processing.")
