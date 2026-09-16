import pytest

from helpers import generate_user_data, register_user, login_user, delete_user


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def registered_user(user_data):
    register_user(user_data)
    yield user_data
    login_response = login_user({
        "email": user_data["email"],
        "password": user_data["password"],
    })
    token = login_response.json().get("accessToken")
    delete_user({"Authorization": token})


@pytest.fixture
def auth_headers(user_data):
    register_user(user_data)
    login_response = login_user({
        "email": user_data["email"],
        "password": user_data["password"],
    })
    token = login_response.json()["accessToken"]
    headers = {"Authorization": token}
    yield headers
    delete_user(headers)
