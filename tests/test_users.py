import pytest

from app import schemas


def test_create_user(client):
    res = client.post(
        "/users",
        json={
            "email": "hello123@example.com",
            "password": "password123",
            "phone_number": "+14155552671",
        },
    )

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "hello123@example.com"


def test_get_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert res.status_code == 200
    assert res.json()["email"] == test_user["email"]


def test_get_user_not_found(client):
    res = client.get("/users/88888")
    assert res.status_code == 404


def test_login_user(client, test_user):
    res = client.post(
        "/auth/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    assert res.status_code == 200
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrong@example.com", "password123", 403),
        ("test@example.com", "wrongpassword", 403),
        ("wrong@example.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("test@example.com", None, 422),
    ],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/auth/login", data={"username": email, "password": password})
    assert res.status_code == status_code
