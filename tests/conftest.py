import pytest
import requests

from helpers import generate_user_data
from urls import REGISTER_URL, LOGIN_URL, USER_URL


@pytest.fixture
def user_data():
    """Возвращает данные для нового пользователя, но не создаёт его."""
    return generate_user_data()


@pytest.fixture
def registered_user(user_data):
    """Создаёт пользователя через API, возвращает данные + токены.
    После теста удаляет пользователя через API (cleanup)."""
    response = requests.post(REGISTER_URL, json=user_data)
    tokens = response.json()

    yield {
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "accessToken": tokens.get("accessToken"),
        "refreshToken": tokens.get("refreshToken"),
    }

    # Cleanup: удаляем пользователя
    access_token = tokens.get("accessToken")
    if access_token:
        headers = {"Authorization": access_token}
        requests.delete(USER_URL, headers=headers)


@pytest.fixture
def auth_headers(registered_user):
    """Возвращает заголовки с токеном авторизации."""
    return {"Authorization": registered_user["accessToken"]}
