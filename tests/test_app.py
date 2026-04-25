from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_root_redirects_to_static_index():
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities():
    # Arrange
    expected_activity_keys = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activity_keys
    assert response.json()["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_appends_participant():
    # Arrange
    activity_name = "Chess Club"
    email = "teststudent@mergington.edu"
    original_participants = activities[activity_name]["participants"].copy()

    try:
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
        assert email in activities[activity_name]["participants"]
    finally:
        activities[activity_name]["participants"] = original_participants


def test_signup_for_missing_activity_returns_404():
    # Arrange
    activity_name = "Nonexistent Activity"
    email = "missingstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
