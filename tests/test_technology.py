def test_create_and_get_technology(test_client, user_token):
    create_response = test_client.post(
        "/app/tech/",
        json={"name": "Python", "category": "Programming", "about": "A versatile language."},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert create_response.status_code == 201
    technology = create_response.json()
    assert technology["name"] == "Python"
    assert technology["category"] == "Programming"

    get_response = test_client.get("/app/tech/Python")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "Python"


def test_update_technology_and_filter_list(test_client, user_token, admin_token):
    test_client.post(
        "/app/tech/",
        json={"name": "Django", "category": "Framework", "about": "Web framework."},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    update_response = test_client.patch(
        "/app/tech/Django",
        json={"category": "Web Framework", "about": "Full-stack web framework."},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["category"] == "Web Framework"
    assert updated["about"] == "Full-stack web framework."

    list_response = test_client.get("/app/tech/?category=web")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    delete_response = test_client.delete(
        "/app/tech/Django",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert delete_response.status_code == 200


def test_delete_technology_requires_admin(test_client, user_token):
    test_client.post(
        "/app/tech/",
        json={"name": "Flask", "category": "Framework", "about": "Minimal web framework."},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    response = test_client.delete(
        "/app/tech/Flask",
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 403
