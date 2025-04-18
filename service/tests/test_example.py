from fastapi.testclient import TestClient

from app.main import app


def test_root():
    client = TestClient(app)
    response = client.get("/")
    data = response.json()

    assert response.status_code == 200
    assert data["message"] == "OSTDependency backend"
