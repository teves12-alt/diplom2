import pytest
import allure

from helpers import login_user, assert_json
from data import STATUS_OK, STATUS_UNAUTHORIZED, TEXT_INVALID_CREDENTIALS


@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем — 200, success: true")
    def test_login_existing_user_success(self, registered_user):
        response = login_user({
            "email": registered_user["email"],
            "password": registered_user["password"],
        })
        body = assert_json(response)

        assert response.status_code == STATUS_OK
        assert "success" in body, f"В ответе отсутствует поле success: {body}"
        assert body["success"] is True
        assert isinstance(body.get("accessToken"), str), (
            f"accessToken должен быть строкой: {body.get('accessToken')}"
        )
        assert isinstance(body.get("refreshToken"), str), (
            f"refreshToken должен быть строкой: {body.get('refreshToken')}"
        )

        user = body.get("user")
        assert user is not None, f"Ответ не содержит объект user: {body}"
        assert user.get("email") == registered_user["email"], (
            f"Email не совпадает.\nОжидался: {registered_user['email']}\n"
            f"Получен: {user.get('email')}"
        )

    @allure.title("Вход с неверным паролем — 401")
    def test_login_with_wrong_password_fails(self, registered_user):
        response = login_user({
            "email": registered_user["email"],
            "password": "wrong_password_123",
        })
        body = assert_json(response)

        assert response.status_code == STATUS_UNAUTHORIZED
        assert body.get("message") == TEXT_INVALID_CREDENTIALS, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_CREDENTIALS}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

    @allure.title("Вход с несуществующим email — 401")
    def test_login_with_wrong_email_fails(self, registered_user, user_data):
        wrong_email = user_data["email"]
        response = login_user({
            "email": wrong_email,
            "password": registered_user["password"],
        })
        body = assert_json(response)

        assert response.status_code == STATUS_UNAUTHORIZED
        assert body.get("message") == TEXT_INVALID_CREDENTIALS, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_CREDENTIALS}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

    @allure.title("Вход с неверными email и паролем — 401")
    def test_login_with_wrong_email_and_password_fails(self, user_data):
        response = login_user({
            "email": user_data["email"],
            "password": user_data["password"],
        })
        body = assert_json(response)

        assert response.status_code == STATUS_UNAUTHORIZED
        assert body.get("message") == TEXT_INVALID_CREDENTIALS, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_CREDENTIALS}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )
