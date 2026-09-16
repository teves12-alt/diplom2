import pytest
import allure

from helpers import create_order, assert_json, assert_success
from data import (
    STATUS_OK, STATUS_BAD_REQUEST, STATUS_INTERNAL_ERROR,
    TEXT_NO_INGREDIENTS, TEXT_INVALID_HASH,
    INGREDIENT_BUN, INGREDIENT_FILLING, INGREDIENT_INVALID,
)


@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией: {ingredients_desc}")
    @pytest.mark.parametrize("ingredients, ingredients_desc", [
        ([INGREDIENT_BUN, INGREDIENT_FILLING], "булка + начинка"),
        ([INGREDIENT_BUN], "только булка"),
        ([INGREDIENT_FILLING], "только начинка"),
    ])
    def test_create_order_with_auth_and_ingredients(
        self, ingredients, ingredients_desc, auth_headers
    ):
        response = create_order({"ingredients": ingredients}, auth_headers)

        assert response.status_code == STATUS_OK
        body = assert_json(response)
        assert_success(body, True)
        assert "name" in body, f"Ответ не содержит поле name: {body}"
        assert "order" in body, f"Ответ не содержит поле order: {body}"

        order = body["order"]
        assert "number" in order, f"Объект order не содержит поле number: {order}"
        assert "ingredients" in order, (
            f"Объект order не содержит поле ingredients: {order}"
        )
        assert order["ingredients"] == ingredients, (
            f"Ингредиенты в ответе не совпадают с отправленными.\n"
            f"Отправлены: {ingredients}\n"
            f"Получены: {order['ingredients']}"
        )

    @allure.title("Создание заказа без авторизации с валидными ингредиентами")
    def test_create_order_without_auth_with_ingredients(self):
        response = create_order({"ingredients": [INGREDIENT_BUN, INGREDIENT_FILLING]})

        assert response.status_code == STATUS_OK
        body = assert_json(response)
        assert_success(body, True)
        assert "name" in body, f"Ответ не содержит поле name: {body}"

        order = body["order"]
        assert "number" in order, f"Объект order не содержит поле number: {order}"

    @allure.title("Создание заказа без ингредиентов с авторизацией — 400")
    def test_create_order_without_ingredients_with_auth(self, auth_headers):
        response = create_order({"ingredients": []}, auth_headers)

        assert response.status_code == STATUS_BAD_REQUEST
        body = assert_json(response)
        assert_success(body, False)
        assert body.get("message") == TEXT_NO_INGREDIENTS, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_NO_INGREDIENTS}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

    @allure.title("Создание заказа без ингредиентов без авторизации — 400")
    def test_create_order_without_ingredients_without_auth(self):
        response = create_order({"ingredients": []})

        assert response.status_code == STATUS_BAD_REQUEST
        body = assert_json(response)
        assert_success(body, False)
        assert body.get("message") == TEXT_NO_INGREDIENTS, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_NO_INGREDIENTS}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

    @allure.title("Создание заказа с неверным хешем с авторизацией — 500")
    def test_create_order_with_invalid_hash_with_auth(self, auth_headers):
        response = create_order({"ingredients": [INGREDIENT_INVALID]}, auth_headers)

        assert response.status_code == STATUS_INTERNAL_ERROR
        body = assert_json(response)
        assert_success(body, False)
        assert body.get("message") == TEXT_INVALID_HASH, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_HASH}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

    @allure.title("Создание заказа с неверным хешем без авторизации — 500")
    def test_create_order_with_invalid_hash_without_auth(self):
        response = create_order({"ingredients": [INGREDIENT_INVALID]})

        assert response.status_code == STATUS_INTERNAL_ERROR
        body = assert_json(response)
        assert_success(body, False)
        assert body.get("message") == TEXT_INVALID_HASH, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_HASH}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

