import pytest
import allure
from api.client import ApiClient
from data.test_data import generate_random_email, generate_random_password, generate_random_name
import time


@pytest.fixture(scope="session")
def api_client():
    """Фикстура, предоставляющая экземпляр ApiClient для всех тестов."""
    return ApiClient()


@pytest.fixture
def random_user_data():
    """Фикстура, генерирующая случайные данные для регистрации пользователя."""
    email = generate_random_email()
    password = generate_random_password()
    name = generate_random_name()
    return {"email": email, "password": password, "name": name}


@pytest.fixture
def registered_user(api_client, random_user_data):
    """
    Фикстура, регистрирующая пользователя перед тестом и удаляющая его после.
    Возвращает данные пользователя и токен доступа.
    """
    email = random_user_data["email"]
    password = random_user_data["password"]
    name = random_user_data["name"]

    with allure.step(f"Регистрация пользователя: {email}"):
        response = api_client.register_user(email, password, name)
        assert response.status_code == 200, f"Ошибка при регистрации: {response.text}"
        token = response.json()["accessToken"]

    yield email, password, name, token

    with allure.step(f"Удаление пользователя: {email}"):
        if token:
            response = api_client.delete_user(token)
            # Иногда API возвращает 404, если пользователь уже удален,
            # но для демонстрации можно добавить проверку 202
            # assert response.status_code == 202, f"Ошибка при удалении пользователя: {response.text}"
            print(f"\nUser {email} deleted. Status: {response.status_code}")
            time.sleep(1)  # Небольшая задержка, чтобы избежать Rate Limit


@pytest.fixture(scope="session")
def get_some_ingredients_ids(api_client):
    """
    Фикстура, получающая ID нескольких ингредиентов (булка, соус, начинка)
    для создания заказа. Выполняется один раз за тестовую сессию.
    """
    with allure.step("Получение ID ингредиентов"):
        response = api_client.get_ingredients()
        assert response.status_code == 200, f"Ошибка при получении ингредиентов: {response.text}"
        ingredients_data = response.json()["data"]

        bun_id = None
        sauce_id = None
        main_id = None

        # Ищем по одному ингредиенту каждого типа
        for item in ingredients_data:
            if item["type"] == "bun" and bun_id is None:
                bun_id = item["_id"]
            elif item["type"] == "sauce" and sauce_id is None:
                sauce_id = item["_id"]
            elif item["type"] == "main" and main_id is None:
                main_id = item["_id"]
            if bun_id and sauce_id and main_id:
                break

        if not (bun_id and sauce_id and main_id):
            pytest.fail("Не удалось найти все необходимые типы ингредиентов (булка, соус, начинка).")

        return [bun_id, sauce_id, main_id]