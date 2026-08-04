def test_create_course_admin_only(test_client, user_token, admin_token):
    test_client.post(
        "/app/tech/",
        json={"name": "FastAPI", "category": "Framework", "about": "Fast API framework."},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    create_response = test_client.post(
        "/app/course/",
        json={"title": "FastAPI Mastery", "description": "Advanced FastAPI training.", "technology_name": "FastAPI"},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert create_response.status_code == 201
    course = create_response.json()
    assert course["title"] == "FastAPI Mastery"
    assert course["technology_name"] == "FastAPI"

    list_response = test_client.get("/app/course/")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    get_response = test_client.get("/app/course/FastAPI%20Mastery")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "FastAPI Mastery"

    patch_response = test_client.patch(
        "/app/course/FastAPI%20Mastery",
        json={"description": "Updated advanced training."},
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert patch_response.status_code == 200
    assert patch_response.json()["description"] == "Updated advanced training."

    delete_response = test_client.delete(
        "/app/course/FastAPI%20Mastery",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert delete_response.status_code == 200


def test_non_admin_cannot_create_course(test_client, user_token):
    test_client.post(
        "/app/tech/",
        json={"name": "SQLAlchemy", "category": "ORM", "about": "ORM library."},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    response = test_client.post(
        "/app/course/",
        json={"title": "SQLAlchemy Deep Dive", "description": "ORM internals.", "technology_name": "SQLAlchemy"},
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 403
