from fastapi.testclient import TestClient
from main import app
import json

test_client = TestClient(app)

def test_check():
    res = test_client.get("/check")
    assert res.status_code == 200
    healthcheck = json.loads(str(res.content, "utf-8"))

    assert healthcheck["message"] == "Server Ready"
    assert healthcheck["database_status"] == "Connected"
    assert "timestamp" in healthcheck