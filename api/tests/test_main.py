from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from api.controllers.employee_controller import get_employee_repository
from api.main import app
from api.models.employee import EmployeeResponse
from api.repositories.employee_repository import (
    EmployeeAlreadyExistsError,
    EmployeeRepository,
)


client = TestClient(app, raise_server_exceptions=False)


@pytest.fixture(name="repository")
def repository_fixture():
    repository = Mock(spec=EmployeeRepository)
    app.dependency_overrides[get_employee_repository] = lambda: repository
    yield repository
    app.dependency_overrides.clear()


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"status": "FastAPI is running"}


def test_create_employee(repository):
    repository.create.return_value = EmployeeResponse(
        id=1,
        name="John Doe",
        email="john.doe@example.com",
        position="Software Engineer",
    )

    response = client.post(
        "/api/employees",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "position": "Software Engineer",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "position": "Software Engineer",
    }
    repository.create.assert_called_once()


@pytest.mark.parametrize(
    "request_body",
    [
        {"email": "john.doe@example.com", "position": "Software Engineer"},
        {"name": "", "email": "john.doe@example.com", "position": "Engineer"},
        {"name": "John Doe", "email": "invalid", "position": "Engineer"},
        {"name": "John Doe", "email": "john.doe@example.com", "position": ""},
    ],
)
def test_create_employee_with_invalid_body_returns_400(repository, request_body):
    response = client.post("/api/employees", json=request_body)

    assert response.status_code == 400
    assert response.json() == {"error": "Invalid request body"}
    repository.create.assert_not_called()


def test_create_employee_when_repository_fails_returns_500(repository):
    repository.create.side_effect = RuntimeError("database unavailable")

    response = client.post(
        "/api/employees",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "position": "Software Engineer",
        },
    )

    assert response.status_code == 500
    assert response.json() == {"error": "Internal server error"}


def test_create_employee_with_duplicate_email_returns_400(repository):
    repository.create.side_effect = EmployeeAlreadyExistsError()

    response = client.post(
        "/api/employees",
        json={
            "name": "John Doe",
            "email": "john.doe@example.com",
            "position": "Software Engineer",
        },
    )

    assert response.status_code == 400
    assert response.json() == {"error": "Invalid request body"}