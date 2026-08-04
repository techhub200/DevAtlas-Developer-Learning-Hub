def test_list_recommendations_empty(test_client):
    response = test_client.get("/app/recommendations/")
    assert response.status_code == 200
    assert response.json() == {"total": 0, "items": []}


def test_admin_can_create_and_delete_recommendation(test_client, admin_token):
    create_response = test_client.post(
        "/app/recommendations/",
        json={
            "description": "An excellent resource to learn FastAPI.",
            "resource_url": "https://fastapi.tiangolo.com/",
            "resource_type": "Article",
        },
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert create_response.status_code == 201
    recommendation = create_response.json()
    assert recommendation["resource_type"] == "Article"

    list_response = test_client.get("/app/recommendations/")
    assert list_response.status_code == 200
    assert list_response.json()["total"] == 1

    delete_response = test_client.delete(
        f"/app/recommendations/{recommendation['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert delete_response.status_code == 200
    assert "deleted successfully" in delete_response.json()["message"]


def test_recommendation_create_forbidden_for_non_admin(test_client, user_token):
    response = test_client.post(
        "/app/recommendations/",
        json={
            "description": "Another resource.",
            "resource_url": "https://example.com/",
            "resource_type": "Technology",
        },
        headers={"Authorization": f"Bearer {user_token}"},
    )

    assert response.status_code == 403
