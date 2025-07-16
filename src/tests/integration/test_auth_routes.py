import pytest

@pytest.mark.asyncio
async def test_register_and_login(client):
    response = await client.post("/api/v1/auth/register", json={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

    response = await client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

    response = await client.post("/api/v1/auth/login", data={
        "username": "testuser",
        "password": "wrongpassword"
    })
    assert response.status_code == 401
