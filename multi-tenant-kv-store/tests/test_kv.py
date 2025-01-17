import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

@pytest.fixture
def token():
    client.post("/auth/signup", json={"email": "test_kv@cambai.com", "password": "secret"})
    login_resp = client.post("/auth/login", data={"username": "test_kv@cambai.com", "password": "secret"})
    return login_resp.json()["access_token"]

def test_kv_crud(token):
    headers = {"Authorization": f"Bearer {token}"}

    # Create
    resp = client.post("/kv/", json={"key": "mykey", "value": "myvalue"}, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["key"] == "mykey"
    assert data["value"] == "myvalue"

    # Read
    resp = client.get("/kv/mykey", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["key"] == "mykey"
    assert data["value"] == "myvalue"

    # Update
    resp = client.put("/kv/", json={"key": "mykey", "value": "updatedvalue"}, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["value"] == "updatedvalue"

    # Delete
#     delete(
#     url,
#     *,
#     params=None,
#     headers=None,
#     cookies=None,
#     auth=USE_CLIENT_DEFAULT,
#     follow_redirects=None,
#     allow_redirects=None,
#     timeout=USE_CLIENT_DEFAULT,
#     extensions=None
# )
    resp = client.delete("/kv/mykey", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Key 'mykey' deleted successfully."
