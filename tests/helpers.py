import random
import string

import allure
import requests

from urls import REGISTER_URL, LOGIN_URL, ORDERS_URL, DELETE_USER_URL
from data import MAX_LOG_LENGTH


def generate_user_data():
    """Генерирует случайные данные для создания пользователя."""
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return {
        "email": f"test_{suffix}@test.com",
        "password": f"pass_{suffix}",
        "name": f"User_{suffix}",
    }


@allure.step("Регистрация пользователя")
def register_user(payload):
    return requests.post(REGISTER_URL, json=payload)


@allure.step("Авторизация пользователя")
def login_user(payload):
    return requests.post(LOGIN_URL, json=payload)


@allure.step("Создание заказа")
def create_order(payload, headers=None):
    return requests.post(ORDERS_URL, json=payload, headers=headers)


@allure.step("Удаление пользователя")
def delete_user(headers):
    return requests.delete(DELETE_USER_URL, headers=headers)


@allure.step("Проверка и парсинг JSON-ответа")
def assert_json(response):
    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        f"Ожидался JSON, но получен Content-Type: {content_type}.\n"
        f"Метод: {response.request.method}, URL: {response.url}\n"
        f"Тело ответа: {response.text[:MAX_LOG_LENGTH]}"
    )
    body = response.json()
    assert body is not None, f"Тело ответа пустое: {response.text[:MAX_LOG_LENGTH]}"
    return body


@allure.step("Проверка поля success")
def assert_success(body, expected):
    assert "success" in body, f"В ответе отсутствует поле success: {body}"
    assert body["success"] is expected, (
        f"Ожидался success={expected}, получен: {body['success']}. Тело: {body}"
    )

