import pytest
import allure
import requests

from helpers import generate_user_data
from urls import LOGIN_URL
from data import STATUS_OK, STATUS_UNAUTHORIZED, TEXT_INVALID_CREDENTIALS


def _assert_json(response):
    """Проверяет Content-Type и парсит JSON с понятным контекстом при ошибке."""
    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        f"Ожидался JSON, но получен Content-Type: {content_type}.\n"
        f"Метод: {response.request.method}, URL: {response.url}\n"
        f"Тело: {response.text[:500]}"
    )
    try:
        return response.json()
    except ValueError:
        raise AssertionError(
            f"Не удалось распарсить JSON.\n"
            f"Метод: {response.request.method}, URL: {response.url}\n"
            f"Тело: {response.text[:500]}"
        )


@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем — 200, success: true")
    def test_login_existing_user_success(self, registered_user):
        with allure.step("Отправить запрос на логин"):
            response = requests.post(LOGIN_URL, json={
                "email": registered_user["email"],
                "password": registered_user["password"],
            })
            body = _assert_json(response)

        with allure.step("Проверить статус-код и поле success"):
            assert response.status_code == STATUS_OK
            assert "success" in body, f"В ответе отсутствует поле success: {body}"
            assert body["success"] is True

        with allure.step("Проверить наличие токенов"):
            assert isinstance(body.get("accessToken"), str), (
                f"accessToken должен быть строкой: {body.get('accessToken')}"
            )
            assert isinstance(body.get("refreshToken"), str), (
                f"refreshToken должен быть строкой: {body.get('refreshToken')}"
            )

        with allure.step("Проверить данные пользователя в ответе"):
            user = body.get("user")
            assert user is not None, f"Ответ не содержит объект user: {body}"
            assert user.get("email") == registered_user["email"], (
                f"Email не совпадает.\nОжидался: {registered_user['email']}\n"
                f"Получен: {user.get('email')}"
            )

    @allure.title("Вход с неверным паролем — 401")
    def test_login_with_wrong_password_fails(self, registered_user):
        payload = {
            "email": registered_user["email"],
            "password": "wrong_password_123",
        }

        with allure.step("Отправить запрос с неверным паролем"):
            response = requests.post(LOGIN_URL, json=payload)
            body = _assert_json(response)

        with allure.step("Проверить статус-код и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("message") == TEXT_INVALID_CREDENTIALS, (
                f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_CREDENTIALS}\n"
                f"Получен: {body.get('message')}. Тело: {body}"
            )

    @allure.title("Вход с неверным email — 401")
    def test_login_with_wrong_email_fails(self, registered_user, user_data):
        # Генерируем гарантированно несуществующий email
        wrong_email = user_data["email"]

        with allure.step("Отправить запрос с несуществующим email"):
            response = requests.post(LOGIN_URL, json={
                "email": wrong_email,
                "password": registered_user["password"],
            })
            body = _assert_json(response)

        with allure.step("Проверить статус-код и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("message") == TEXT_INVALID_CREDENTIALS, (
                f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_CREDENTIALS}\n"
                f"Получен: {body.get('message')}. Тело: {body}"
            )

    @allure.title("Вход с неверными email и паролем — 401")
    def test_login_with_wrong_email_and_password_fails(self, user_data):
        # Используем сгенерированные данные — пользователь с такими не зарегистрирован
        payload = {
            "email": user_data["email"],
            "password": user_data["password"],
        }

        with allure.step("Отправить запрос с полностью неверными учётными данными"):
            response = requests.post(LOGIN_URL, json=payload)
            body = _assert_json(response)

        with allure.step("Проверить статус-код и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("message") == TEXT_INVALID_CREDENTIALS, (
                f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_CREDENTIALS}\n"
                f"Получен: {body.get('message')}. Тело: {body}"
            )
