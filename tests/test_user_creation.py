import pytest
import allure

from helpers import register_user, assert_json
from data import STATUS_OK, STATUS_FORBIDDEN, TEXT_USER_EXISTS, TEXT_MISSING_FIELDS


@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя — 200, success: true")
    def test_create_unique_user_success(self, user_data):
        response = register_user(user_data)
        body = assert_json(response)

        assert response.status_code == STATUS_OK
        assert "success" in body, f"В ответе отсутствует поле success: {body}"
        assert body["success"] is True

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
        assert isinstance(body.get("accessToken"), str), (
            f"accessToken должен быть строкой: {body.get('accessToken')}"
        )
        assert isinstance(body.get("refreshToken"), str), (
            f"refreshToken должен быть строкой: {body.get('refreshToken')}"
        )

    @allure.title("Создание уже зарегистрированного пользователя — 403")
    def test_create_duplicate_user_fails(self, registered_user):
        response = register_user({
            "email": registered_user["email"],
            "password": registered_user["password"],
            "name": registered_user["name"],
        })
        body = assert_json(response)

        assert response.status_code == STATUS_FORBIDDEN
        assert body.get("message") == TEXT_USER_EXISTS, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_USER_EXISTS}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

    @allure.title("Создание пользователя без поля '{missing_field}' — 403")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field_fails(self, missing_field, user_data):
        payload = {k: v for k, v in user_data.items() if k != missing_field}
        response = register_user(payload)
        body = assert_json(response)

        assert response.status_code == STATUS_FORBIDDEN
        assert body.get("message") == TEXT_MISSING_FIELDS, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_MISSING_FIELDS}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )
