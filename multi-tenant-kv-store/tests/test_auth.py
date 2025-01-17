import pytest
from fastapi.testclient import TestClient
from src.main import app

#https://fastapi.tiangolo.com/reference/testclient/
# TestClient(
#     app,
#     base_url="http://testserver",
#     raise_server_exceptions=True,
#     root_path="",
#     backend="asyncio",
#     backend_options=None,
#     cookies=None,
#     headers=None,
#     follow_redirects=True,
# )


client = TestClient(app)

def test_signup_login():
    # 1) Sign up a new tenant
#     post(
#     url,
#     *,
#     content=None,
#     data=None,
#     files=None,
#     json=None,
#     params=None,
#     headers=None,
#     cookies=None,
#     auth=USE_CLIENT_DEFAULT,
#     follow_redirects=None,
#     allow_redirects=None,
#     timeout=USE_CLIENT_DEFAULT,
#     extensions=None
# )
    response = client.post("/auth/signup", json={"email": "testuser@cambai.com", "password": "xxxxx"})
    assert response.status_code in [200, 201, 400], f"Unexpected status: {response.status_code}"
    if response.status_code == 200:
        data = response.json()
        assert "Tenant created with ID:" in data["message"]


    response = client.post("/auth/login", data={"username": "testuser@cambai.com", "password": "txxxxx"})
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data

def test_login_invalid():
    response = client.post("/auth/login", data={"username": "nope@cambai.com", "password": "xxxxxxx"})
    assert response.status_code == 401



