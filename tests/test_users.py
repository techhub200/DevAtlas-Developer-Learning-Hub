from src.database.schemas import User


def test_get_profile_returns_current_user(test_client, user_token):
    response = test_client.get(
        "/app/users/Profile",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user@example.com"
    assert data["username"] == "user1"


def test_update_profile_fields(test_client, user_token):
    update_payload = {
        "bio": "Updated test bio",
        "phone_number": "0987654321",
        "email": "updated@example.com",
    }

    response = test_client.put(
        "/app/users/Update_Profile",
        json=update_payload,
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "Updated test bio"
    assert data["email"] == "updated@example.com"
    assert data["phone_number"] == "0987654321"


def test_grant_admin_is_restricted_for_non_admin(test_client, db_session, user_token):
    register_response = test_client.post(
        "/app/auth/Register",
        json={"email": "grantme@example.com", "username": "grantme", "password": "Password123!"},
    )
    assert register_response.status_code == 201
    user = db_session.query(User).filter(User.email == "grantme@example.com").first()

    response = test_client.put(
        "/app/users/grant-admin",
        json={"user_id": user.id},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 403


def test_admin_can_grant_admin_permissions(test_client, admin_token, db_session):
    register_response = test_client.post(
        "/app/auth/Register",
        json={"email": "seconduser@example.com", "username": "seconduser", "password": "Password123!"},
    )
    assert register_response.status_code == 201
    target_user = db_session.query(User).filter(User.email == "seconduser@example.com").first()

    response = test_client.put(
        "/app/users/grant-admin",
        json={"user_id": target_user.id},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["is_admin"] is True
    assert body["user_id"] == target_user.id

    db_session.expire(target_user)
    db_session.refresh(target_user)
    assert target_user.is_admin is True
