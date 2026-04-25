import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    # Reset activities to initial state before each test
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    })
    return TestClient(app)


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activity_keys = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert set(response.json().keys()) == expected_activity_keys
    assert response.json()["Chess Club"]["max_participants"] == 12


def test_signup_for_activity_appends_participant(client):
    # Arrange
    activity_name = "Chess Club"
    payload = {"email": "teststudent@mergington.edu"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {payload['email']} for {activity_name}"}
    assert payload["email"] in activities[activity_name]["participants"]


def test_signup_for_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Activity"
    payload = {"email": "missingstudent@mergington.edu"}

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_without_email_returns_422(client):
    # Arrange
    activity_name = "Chess Club"
    payload = {}  # Missing email

    # Act
    response = client.post(f"/activities/{activity_name}/signup", json=payload)

    # Assert
    assert response.status_code == 422
