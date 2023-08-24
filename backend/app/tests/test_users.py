from fastapi.testclient import TestClient
from app.main import app
from app.models.users import UserCreate
from app.core.database import get_db, get_test_db, Base, test_engine
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
        remember_token="token", 
        recipient_email="test@email.com"
    )

# Test user signup
def test_signup(test_client, test_user, override_get_db):
    response = test_client.post("/users/signup/", json=test_user.model_dump())
    assert response.status_code == 200
    assert "username" in response.json()

# Test user signup with an existing username
def test_signup_existing_username(test_client, test_user, override_get_db):
    test_client.post("/users/signup/", json=test_user.model_dump())
    response = test_client.post("/users/signup/", json=test_user.model_dump())
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

# Test user signup with an existing email
def test_signup_existing_email(test_client, test_user, override_get_db):
    test_client.post("/users/signup/", json=test_user.model_dump())
    test_user.username = "newusername"
    response = test_client.post("/users/signup/", json=test_user.model_dump())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

# Test user login
def test_signin(test_client, test_user, override_get_db):
    test_client.post("/users/signup/", json=test_user.model_dump())
    response = test_client.post("/users/signin/", data={"username": test_user.username, "password": test_user.password})
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test user login with incorrect password
def test_signin_incorrect_password(test_client, test_user, override_get_db):
    test_client.post("/users/signup/", json=test_user.model_dump())
    response = test_client.post("/users/signin/", data={"username": test_user.username, "password": "wrongpassword"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"

# Test user login with non-existing user
def test_signin_non_existing_user(test_client, override_get_db):
    response = test_client.post("/users/signin/", data={"username": "nonexistent", "password": "password123"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"