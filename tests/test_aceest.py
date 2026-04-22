from pathlib import Path
import py_compile

from ACEest_Fitness import app


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["health"] == "ok"


def test_home_ui_page():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"ACEest Fitness & Gym" in response.data


def test_api_home_endpoint():
    client = app.test_client()
    response = client.get("/api")
    assert response.status_code == 200
    assert response.get_json()["service"] == "devops-cicd-assignment"


def test_versions_endpoint():
    client = app.test_client()
    response = client.get("/versions")
    payload = response.get_json()
    assert response.status_code == 200
    assert "Aceestver-1.0.py" in payload["versions"]
    assert "Aceestver-3.2.4.py" in payload["versions"]


def test_uploaded_version_files_exist():
    expected_files = [
        "Aceestver-1.0.py",
        "Aceestver-1.1.py",
        "Aceestver1.1.2.py",
        "Aceestver2.0.1.py",
        "Aceestver-2.1.2.py",
        "Aceestver-2.2.1.py",
        "Aceestver-2.2.4.py",
        "Aceestver-3.0.1.py",
        "Aceestver-3.1.2.py",
        "Aceestver-3.2.4.py",
    ]
    for file_name in expected_files:
        assert Path(file_name).exists()


def test_uploaded_versions_are_syntax_valid():
    for file_path in Path(".").glob("Aceestver*.py"):
        py_compile.compile(str(file_path), doraise=True)
