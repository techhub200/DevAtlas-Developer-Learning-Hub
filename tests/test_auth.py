from src.api.auth import routes as auth_routes


def test_register_user_success(test_client):
    payload = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "Password123!",
        "bio": "A short bio",
        "phone_number": "1234567890",
    }

    response = test_client.post("/app/auth/Register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "User registered successfully"
    assert isinstance(data["user_id"], int)


def test_register_user_duplicate_email(test_client):
    payload = {
        "email": "duplicate@example.com",
        "username": "user-a",
        "password": "Password123!",
    }
    test_client.post("/app/auth/Register", json=payload)

    response = test_client.post(
        "/app/auth/Register",
        json={"email": "duplicate@example.com", "username": "user-b", "password": "Password123!"},
    )

    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]


def test_login_user_success(test_client):
    registration = test_client.post(
        "/app/auth/Register",
        json={"email": "login@example.com", "username": "loginuser", "password": "Password123!"},
    )
    assert registration.status_code == 201

    response = test_client.post(
        "/app/auth/login",
        json={"email": "login@example.com", "password": "Password123!"},
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_login_user_invalid_password(test_client):
    test_client.post(
        "/app/auth/Register",
        json={"email": "invalidpass@example.com", "username": "invalidpass", "password": "Password123!"},
    )

    response = test_client.post(
        "/app/auth/login",
        json={"email": "invalidpass@example.com", "password": "wrongpass"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"


def test_logout_revokes_token(test_client, monkeypatch):
    test_client.post(
        "/app/auth/Register",
        json={"email": "logout@example.com", "username": "logoutuser", "password": "Password123!"},
    )
    login_response = test_client.post(
        "/app/auth/login",
        json={"email": "logout@example.com", "password": "Password123!"},
    )
    token = login_response.json()["access_token"]

    monkeypatch.setattr(auth_routes, "add_access_token_to_blacklist", lambda jti, exp: None)

    response = test_client.post(
        "/app/auth/Logout",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out (access token revoked)"
