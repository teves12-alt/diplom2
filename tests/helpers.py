import random
import string
import requests


def assert_successful_response(response: requests.Response, required_fields=None):
    """Проверяет, что ответ успешен и содержит JSON с нужными полями.

    Параметры:
        response — объект ответа requests
        required_fields — список ключей, которые обязаны быть в теле

    Если статус не 200 — падает с телом ответа.
    Если Content-Type не JSON — падает с понятным сообщением.
    Если тело пустое или поле отсутствует — падает с указанием поля.
    """
    assert response.status_code == 200, (
        f"Ожидался статус 200, получен {response.status_code}. "
        f"Ответ: {response.text}"
    )

    content_type = response.headers.get("Content-Type", "")
    assert content_type.startswith("application/json"), (
        f"Ожидался JSON, получен Content-Type: '{content_type}'. "
        f"Статус: {response.status_code}, тело: {response.text[:500]}"
    )

    body = response.json()
    assert body, (
        f"Тело ответа пустое при статусе 200. "
        f"Content-Type: {content_type}"
    )

    if required_fields:
        for field in required_fields:
            assert field in body, (
                f"В ответе отсутствует обязательное поле '{field}'. "
                f"Тело: {body}"
            )

    return body


from faker import Faker

faker = Faker("ru_RU")


def generate_email():
    """Генерирует уникальный email для каждого теста."""
    return f"test_{faker.word()}_{random.randint(1000, 9999)}@yandex.ru"


def generate_password():
    """Генерирует случайный пароль."""
    return faker.password(length=10)


def generate_name():
    """Генерирует случайное имя."""
    return faker.first_name()


def generate_user_data():
    """Возвращает полный набор валидных данных пользователя."""
    return {
        "email": generate_email(),
        "password": generate_password(),
        "name": generate_name(),
    }
