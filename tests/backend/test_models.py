import pytest
from pydantic import ValidationError
from src.app import Activity, SignupRequest


class TestActivity:
    def test_valid_activity_creation(self):
        # Arrange
        data = {
            "description": "Test activity",
            "schedule": "Daily",
            "max_participants": 10,
            "participants": ["test@example.com"]
        }

        # Act
        activity = Activity(**data)

        # Assert
        assert activity.description == "Test activity"
        assert activity.schedule == "Daily"
        assert activity.max_participants == 10
        assert activity.participants == ["test@example.com"]

    def test_activity_with_empty_participants(self):
        # Arrange
        data = {
            "description": "Empty activity",
            "schedule": "Weekly",
            "max_participants": 5,
            "participants": []
        }

        # Act
        activity = Activity(**data)

        # Assert
        assert activity.participants == []

    def test_activity_invalid_max_participants(self):
        # Arrange
        data = {
            "description": "Invalid max",
            "schedule": "Monthly",
            "max_participants": -1,  # Invalid
            "participants": []
        }

        # Act & Assert
        with pytest.raises(ValidationError):
            Activity(**data)


class TestSignupRequest:
    def test_valid_email(self):
        # Arrange
        data = {"email": "student@school.edu"}

        # Act
        request = SignupRequest(**data)

        # Assert
        assert request.email == "student@school.edu"

    def test_invalid_email(self):
        # Arrange
        data = {"email": "invalid-email"}

        # Act & Assert
        with pytest.raises(ValidationError):
            SignupRequest(**data)

    def test_empty_email(self):
        # Arrange
        data = {"email": ""}

        # Act & Assert
        with pytest.raises(ValidationError):
            SignupRequest(**data)