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


class TestRootEndpoint:
    def test_root_redirects_to_static_index(self, client):
        # Arrange - client fixture

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    def test_get_activities_returns_all_activities(self, client):
        # Arrange - client fixture

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert data["Chess Club"]["max_participants"] == 12
        assert len(data["Chess Club"]["participants"]) == 2


class TestSignupEndpoint:
    def test_signup_for_activity_success(self, client):
        # Arrange
        activity_name = "Chess Club"
        payload = {"email": "newstudent@mergington.edu"}

        # Act
        response = client.post(f"/activities/{activity_name}/signup", json=payload)

        # Assert
        assert response.status_code == 200
        assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]
        # Verify participant was added
        activities_response = client.get("/activities")
        assert "newstudent@mergington.edu" in activities_response.json()[activity_name]["participants"]

    def test_signup_for_missing_activity_returns_404(self, client):
        # Arrange
        activity_name = "Nonexistent Activity"
        payload = {"email": "student@mergington.edu"}

        # Act
        response = client.post(f"/activities/{activity_name}/signup", json=payload)

        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_without_email_returns_422(self, client):
        # Arrange
        activity_name = "Chess Club"
        payload = {}  # Missing email

        # Act
        response = client.post(f"/activities/{activity_name}/signup", json=payload)

        # Assert
        assert response.status_code == 422

    def test_signup_with_invalid_email_returns_422(self, client):
        # Arrange
        activity_name = "Chess Club"
        payload = {"email": "invalid-email"}

        # Act
        response = client.post(f"/activities/{activity_name}/signup", json=payload)

        # Assert
        assert response.status_code == 422

    def test_signup_at_capacity_returns_400(self, client):
        # Arrange - fill Chess Club to capacity (max 12, currently 2)
        activity_name = "Chess Club"
        for i in range(10):
            payload = {"email": f"student{i}@mergington.edu"}
            client.post(f"/activities/{activity_name}/signup", json=payload)

        # Now at capacity, try to add one more
        payload = {"email": "overcapacity@mergington.edu"}

        # Act
        response = client.post(f"/activities/{activity_name}/signup", json=payload)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Activity is at maximum capacity"

    def test_signup_duplicate_email_returns_400(self, client):
        # Arrange
        activity_name = "Chess Club"
        payload = {"email": "michael@mergington.edu"}  # Already signed up

        # Act
        response = client.post(f"/activities/{activity_name}/signup", json=payload)

        # Assert
        assert response.status_code == 400
        assert response.json()["detail"] == "Email already signed up for this activity"