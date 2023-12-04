from fastapi.testclient import TestClient
from app.main import app
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
def test_user():
    return UserCreate(
        username="testuser",
        password="password123",
        recipient_email="test@email.com",
        turnstile_response="testToken",
    )


@pytest.fixture
def authenticated_client(test_client, test_user, override_get_db):
    response = test_client.post("/users/signup/", json=test_user.model_dump())
    access_token = create_access_token(data={"sub": test_user.username})
    test_client.headers = {"Authorization": f"Bearer {access_token}"}
    return test_client


# POST /signup/ Testing user signup
def test_signup(test_client, test_user, override_get_db):
    response = test_client.post("/users/signup/", json=test_user.model_dump())
    assert response.status_code == 201
    assert "username" in response.json()


# POST /signup/ Test user signup with an existing username
def test_signup_existing_username(test_client, test_user, override_get_db):
    test_client.post("/users/signup/", json=test_user.model_dump())
    response = test_client.post("/users/signup/", json=test_user.model_dump())
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


# POST /signup/ Test user signup with an existing email
def test_signup_existing_email(test_client, test_user, override_get_db):
    test_client.post("/users/signup/", json=test_user.model_dump())
    test_user.username = "newusername"
    response = test_client.post("/users/signup/", json=test_user.model_dump())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


# POST /signin/ Testing user login
def test_signin(test_client, test_user, override_get_db):
    test_client.post("/users/signup/", json=test_user.model_dump())
    response = test_client.post(
        "/users/signin/",
        data={"username": test_user.username, "password": test_user.password},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


# POST /signin/ Test user login with incorrect password
def test_signin_incorrect_password(test_client, test_user, override_get_db):
    test_client.post("/users/signup/", json=test_user.model_dump())
    response = test_client.post(
        "/users/signin/",
        data={"username": test_user.username, "password": "wrongpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


# POST /signin/ Test user login with non-existing user
def test_signin_non_existing_user(test_client, override_get_db):
    response = test_client.post(
        "/users/signin/", data={"username": "nonexistent", "password": "password123"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"


# GET /me/ Retrieve user profile without authentication
def test_get_user_profile_no_auth(test_client):
    response = test_client.get("/users/me/")
    assert response.status_code == 401  # Unauthorized


# GET /me/ Retrieve user profile with valid authentication
def test_get_user_profile_valid_auth(authenticated_client, test_user):
    authenticated_client.post("/users/signup/", json=test_user.model_dump())
    response = authenticated_client.get("/users/me/")
    assert response.status_code == 200
    assert "username" in response.json()
    assert response.json()["username"] == test_user.username
