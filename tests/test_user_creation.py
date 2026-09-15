import pytest
import allure
import requests

from helpers import generate_user_data
from urls import REGISTER_URL, LOGIN_URL, DELETE_USER_URL
from data import (
    STATUS_OK, STATUS_FORBIDDEN,
    TEXT_USER_EXISTS, TEXT_MISSING_FIELDS,
)


def _assert_json(response):
    """Проверяет Content-Type и парсит JSON с понятным контекстом при ошибке."""
    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        f"Ожидался JSON, но получен Content-Type: {content_type}.\n"
        f"Метод: {response.request.method}, URL: {response.url}\n"
        f"Тело ответа: {response.text[:500]}"
    )
    try:
        return response.json()
    except ValueError:
        raise AssertionError(
            f"Не удалось распарсить JSON.\n"
            f"Метод: {response.request.method}, URL: {response.url}\n"
            f"Тело ответа: {response.text[:500]}"
        )


@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя — 200, success: true")
    def test_create_unique_user_success(self, user_data):
        """Создание уникального пользователя — 200, success: true."""
        with allure.step("Отправить запрос на регистрацию"):
            response = requests.post(REGISTER_URL, json=user_data)
            body = _assert_json(response)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code == STATUS_OK

        with allure.step("Проверить поле success"):
            assert "success" in body, f"В ответе отсутствует поле success: {body}"
            assert body["success"] is True

        with allure.step("Проверить данные пользователя в ответе"):
            user = body.get("user")
            assert user is not None, f"Ответ не содержит объект user: {body}"
            assert user["email"] == user_data["email"], (
                f"Email не совпадает.\nОтправлен: {user_data['email']}\n"
                f"Получен: {user['email']}"
            )
            assert user["name"] == user_data["name"], (
                f"Имя не совпадает.\nОтправлено: {user_data['name']}\n"
                f"Получено: {user['name']}"
            )

        with allure.step("Проверить наличие токенов"):
            assert isinstance(body.get("accessToken"), str), (
                f"accessToken должен быть строкой: {body.get('accessToken')}"
            )
            assert isinstance(body.get("refreshToken"), str), (
                f"refreshToken должен быть строкой: {body.get('refreshToken')}"
            )

    @allure.title("Создание уже зарегистрированного пользователя — 403")
    def test_create_duplicate_user_fails(self, registered_user):
        """Создание уже зарегистрированного пользователя — 403."""
        with allure.step("Отправить запрос на регистрацию дубликата"):
            response = requests.post(REGISTER_URL, json={
                "email": registered_user["email"],
                "password": registered_user["password"],
                "name": registered_user["name"],
            })
            body = _assert_json(response)

        with allure.step("Проверить статус-код и сообщение об ошибке"):
            assert response.status_code == STATUS_FORBIDDEN
            assert body.get("message") == TEXT_USER_EXISTS, (
                f"Текст ошибки не совпадает.\nОжидался: {TEXT_USER_EXISTS}\n"
                f"Получен: {body.get('message')}. Тело: {body}"
            )

    @allure.title("Создание пользователя без поля '{missing_field}' — 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field_fails(self, missing_field, user_data):
        """Создание пользователя без одного из обязательных полей — 403."""
        payload = {k: v for k, v in user_data.items() if k != missing_field}

        with allure.step(f"Отправить запрос без поля {missing_field}"):
            response = requests.post(REGISTER_URL, json=payload)
            body = _assert_json(response)

        with allure.step("Проверить статус-код и сообщение об ошибке"):
            assert response.status_code == STATUS_FORBIDDEN
            assert body.get("message") == TEXT_MISSING_FIELDS, (
                f"Текст ошибки не совпадает.\nОжидался: {TEXT_MISSING_FIELDS}\n"
                f"Получен: {body.get('message')}. Тело: {body}"
            )

