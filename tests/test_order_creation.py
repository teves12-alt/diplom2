import pytest
import allure
import requests

from urls import ORDERS_URL
from data import (
    STATUS_OK, STATUS_BAD_REQUEST, STATUS_INTERNAL_ERROR,
    TEXT_NO_INGREDIENTS, TEXT_INVALID_HASH,
    INGREDIENT_BUN, INGREDIENT_FILLING, INGREDIENT_INVALID,
)


def _assert_json(response):
    """Проверяет Content-Type и парсит JSON с подробным контекстом при ошибке."""
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


def _assert_success(body, expected):
    """Проверяет наличие поля success и его значение."""
    assert "success" in body, f"В ответе отсутствует поле success: {body}"
    assert body["success"] is expected, (
        f"Ожидался success={expected}, получен: {body['success']}. Тело: {body}"
    )


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
        response = requests.post(
            ORDERS_URL,
            json={"ingredients": ingredients},
            headers=auth_headers,
        )

        assert response.status_code == STATUS_OK
        body = _assert_json(response)
        _assert_success(body, True)

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
        response = requests.post(
            ORDERS_URL,
            json={"ingredients": [INGREDIENT_BUN, INGREDIENT_FILLING]},
        )

        assert response.status_code == STATUS_OK
        body = _assert_json(response)
        _assert_success(body, True)

        assert "name" in body, f"Ответ не содержит поле name: {body}"
        assert "order" in body, f"Ответ не содержит поле order: {body}"

        order = body["order"]
        assert "number" in order, f"Объект order не содержит поле number: {order}"

    @allure.title("Создание заказа без ингредиентов — 400 (с/без авторизации)")
    @pytest.mark.parametrize("use_auth, expected_status", [
        (True, STATUS_BAD_REQUEST),
        (False, STATUS_BAD_REQUEST),
    ])
    def test_create_order_without_ingredients(self, use_auth, expected_status, auth_headers):
        headers = auth_headers if use_auth else {}

        response = requests.post(
            ORDERS_URL,
            json={"ingredients": []},
            headers=headers,
        )

        assert response.status_code == expected_status
        body = _assert_json(response)
        _assert_success(body, False)
        assert body.get("message") == TEXT_NO_INGREDIENTS, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_NO_INGREDIENTS}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

    @allure.title("Создание заказа с неверным хешем ингредиента — 500 (с/без авторизации)")
    @pytest.mark.parametrize("use_auth, expected_status", [
        (True, STATUS_INTERNAL_ERROR),
        (False, STATUS_INTERNAL_ERROR),
    ])
    def test_create_order_with_invalid_hash(self, use_auth, expected_status, auth_headers):
        headers = auth_headers if use_auth else {}

        response = requests.post(
            ORDERS_URL,
            json={"ingredients": [INGREDIENT_INVALID]},
            headers=headers,
        )

        assert response.status_code == expected_status
        body = _assert_json(response)
        _assert_success(body, False)
        assert body.get("message") == TEXT_INVALID_HASH, (
            f"Текст ошибки не совпадает.\nОжидался: {TEXT_INVALID_HASH}\n"
            f"Получен: {body.get('message')}. Тело: {body}"
        )

