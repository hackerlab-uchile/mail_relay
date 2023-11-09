from fastapi.testclient import TestClient
from app.main import app
from app.models.aliases import AliasBase
from app.models.users import UserCreate
from app.core.database import get_db, get_test_db, Base, test_engine
from app.core.security import create_access_token
import pytest


@pytest.fixture(scope="function")
def override_get_db():
    app.dependency_overrides[get_db] = get_test_db
    yield
    app.dependency_overrides = {}  # Clear out the overrides after the test


@pytest.fixture(scope="function", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=test_engine)
    yield
    for tbl in reversed(Base.metadata.sorted_tables):
        with test_engine.connect() as conn:
            conn.execute(tbl.delete())
            conn.commit()


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def authenticated_client(test_client, test_user, override_get_db):
    response = test_client.post("/users/signup/", json=test_user.model_dump())
    access_token = create_access_token(data={"sub": test_user.username})
    test_client.headers = {"Authorization": f"Bearer {access_token}"}
    return test_client


@pytest.fixture
def test_alias():
    return AliasBase(active=True, description="Test alias")


@pytest.fixture
def test_user():
    return UserCreate(
        username="testuser",
        password="password123",
        recipient_email="test@email.com",
        turnstile_response="testToken",
    )


# GET /aliases/ without authentication
def test_get_aliases_no_auth(test_client):
    response = test_client.get("/aliases/")
    assert response.status_code == 401  # Unauthorized


# GET /aliases/ with authentication but no aliases
def test_get_aliases_empty(authenticated_client):
    response = authenticated_client.get("/aliases/")
    assert len(response.json()) == 0
    assert response.status_code == 200  # No aliases found


# Create an alias and then fetch it
def test_get_aliases_with_data(authenticated_client, test_alias):
    authenticated_client.post("/aliases/", json=test_alias.model_dump())
    response = authenticated_client.get("/aliases/")
    assert response.status_code == 200
    assert len(response.json()) == 1


# POST /aliases/ without authentication
def test_create_alias_no_auth(test_client, test_alias):
    response = test_client.post("/aliases/", json=test_alias.model_dump())
    assert response.status_code == 401  # Unauthorized


# POST /aliases/ with authentication
def test_create_alias(authenticated_client, test_alias):
    response = authenticated_client.post("/aliases/", json=test_alias.model_dump())
    assert response.status_code == 200
    email = response.json()["email"]
    assert email and isinstance(email, str)
    assert "@" in email


# GET /aliases/{alias_id} without authentication
def test_get_specific_alias_no_auth(test_client, test_alias):
    response = test_client.get("/aliases/1/")
    assert response.status_code == 401  # Unauthorized


# GET /aliases/{alias_id} with authentication but wrong ID
def test_get_specific_alias_wrong_id(authenticated_client, test_alias):
    response = authenticated_client.get("/aliases/999/")
    assert response.status_code == 404  # Alias not found


# GET /aliases/{alias_id} with authentication and correct ID
def test_get_specific_alias_correct_id(authenticated_client, test_alias):
    created_alias = authenticated_client.post(
        "/aliases/", json=test_alias.model_dump()
    ).json()
    response = authenticated_client.get(f"/aliases/{created_alias['id']}/")
    assert response.status_code == 200
    returned_alias = response.json()
    assert "email" in returned_alias and isinstance(returned_alias["email"], str)
    assert returned_alias["description"] == test_alias.description


# PUT /aliases/{alias_id} without authentication
def test_update_specific_alias_no_auth(test_client, test_alias):
    updated_alias_data = test_alias.model_dump()
    updated_alias_data["active"] = False
    response = test_client.put("/aliases/1/", json=updated_alias_data)
    assert response.status_code == 401  # Unauthorized


# PUT /aliases/{alias_id} with authentication but wrong ID
def test_update_specific_alias_wrong_id(authenticated_client, test_alias):
    updated_alias_data = test_alias.model_dump()
    updated_alias_data["email"] = "updated@example.com"
    response = authenticated_client.put("/aliases/999/", json=updated_alias_data)
    assert response.status_code == 404  # Alias not found


# PUT /aliases/{alias_id} with authentication and correct ID
def test_update_specific_alias_correct_id(authenticated_client, test_alias):
    created_alias = authenticated_client.post(
        "/aliases/", json=test_alias.model_dump()
    ).json()
    updated_alias_data = test_alias.model_dump()
    updated_alias_data["active"] = False
    response = authenticated_client.put(
        f"/aliases/{created_alias['id']}/", json=updated_alias_data
    )
    assert response.status_code == 200
    assert response.json()["active"] == False


# PUT /aliases/{alias_id} with authentication and correct ID but no data
def test_update_specific_alias_no_data(authenticated_client, test_alias):
    created_alias = authenticated_client.post(
        "/aliases/", json=test_alias.model_dump()
    ).json()
    response = authenticated_client.put(f"/aliases/{created_alias['id']}/", json={})
    assert response.status_code == 200
    assert response.json()["active"] == True


# PUT /aliases/{alias_id} with authentication and correct ID now updating description
def test_update_specific_alias_description(authenticated_client, test_alias):
    created_alias = authenticated_client.post(
        "/aliases/", json=test_alias.model_dump()
    ).json()
    updated_alias_data = test_alias.model_dump()
    updated_alias_data["description"] = "New description"
    response = authenticated_client.put(
        f"/aliases/{created_alias['id']}/", json=updated_alias_data
    )
    assert response.status_code == 200
    assert response.json()["description"] == "New description"


# DELETE /aliases/{alias_id} without authentication
def test_delete_specific_alias_no_auth(test_client):
    response = test_client.delete("/aliases/1/")
    assert response.status_code == 401  # Unauthorized


# DELETE /aliases/{alias_id} with authentication but wrong ID
def test_delete_specific_alias_wrong_id(authenticated_client):
    response = authenticated_client.delete("/aliases/999/")
    assert response.status_code == 404  # Alias not found


# DELETE /aliases/{alias_id} with authentication and correct ID
def test_delete_specific_alias_correct_id(authenticated_client, test_alias):
    created_alias = authenticated_client.post(
        "/aliases/", json=test_alias.model_dump()
    ).json()
    response = authenticated_client.delete(f"/aliases/{created_alias['id']}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Alias deleted."}
