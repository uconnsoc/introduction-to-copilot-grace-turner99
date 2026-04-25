import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


class TestStaticFiles:
    def test_static_css_file_accessible(self, client):
        # Arrange - client fixture

        # Act
        response = client.get("/static/styles.css")

        # Assert
        assert response.status_code == 200
        assert "text/css" in response.headers["content-type"]

    def test_static_js_file_accessible(self, client):
        # Arrange - client fixture

        # Act
        response = client.get("/static/app.js")

        # Assert
        assert response.status_code == 200
        assert "text/javascript" in response.headers["content-type"]

    def test_static_html_file_accessible(self, client):
        # Arrange - client fixture

        # Act
        response = client.get("/static/index.html")

        # Assert
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

    def test_nonexistent_static_file_returns_404(self, client):
        # Arrange - client fixture

        # Act
        response = client.get("/static/nonexistent.txt")

        # Assert
        assert response.status_code == 404