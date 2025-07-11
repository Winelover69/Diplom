import pytest
import allure
from utils.api_client import ApiClient
import random
import string
import time

def generate_random_email():
    return f"test_ui_user_{''.join(random.choices(string.ascii_lowercase + string.digits, k=10))}@example.com"

def generate_random_password():
    return "pass" + ''.join(random.choices(string.digits, k=4))

def generate_random_name():
    return "Name" + ''.join(random.choices(string.ascii_letters, k=5))

@pytest.fixture(scope="module")
def api_client_for_ui_fixtures():
    return ApiClient()

@pytest.fixture(scope="function")
def registered_user_for_ui(api_client_for_ui_fixtures):
    """
    Фикстура для регистрации и удаления пользователя через API для UI тестов.
    Возвращает email, password, name и token.
    """
    email = generate_random_email()
    password = generate_random_password()
    name = generate_random_name()

    with allure.step(f"API: Регистрация пользователя для UI теста: {email}"):
        response = api_client_for_ui_fixtures.register_user(email, password, name)
        assert response.status_code == 200, f"Ошибка при регистрации через API: {response.text}"
        token = response.json()["accessToken"]

    yield email, password, name, token

    with allure.step(f"API: Удаление пользователя после UI теста: {email}"):
        if token:
            response = api_client_for_ui_fixtures.delete_user(token)
            if response.status_code != 202: # API может вернуть 404, если токен протух или пользователь уже удален
                print(f"\nWarning: Could not delete user {email}. Status: {response.status_code}, Response: {response.text}")
            time.sleep(0.5) # Небольшая задержка, чтобы избежать Rate Limit

@pytest.fixture(scope="session")
def get_some_ingredients_names(api_client_for_ui_fixtures):
    """
    Фикстура, получающая названия нескольких ингредиентов (булка, соус, начинка)
    для использования в UI тестах (drag-and-drop).
    """
    with allure.step("API: Получение названий ингредиентов"):
        response = api_client_for_ui_fixtures.get_ingredients()
        assert response.status_code == 200, f"Ошибка при получении ингредиентов: {response.text}"
        ingredients_data = response.json()["data"]

        bun_name = None
        sauce_name = None
        main_name = None

        # Ищем по одному ингредиенту каждого типа
        for item in ingredients_data:
            if item["type"] == "bun" and bun_name is None:
                bun_name = item["name"]
            elif item["type"] == "sauce" and sauce_name is None:
                sauce_name = item["name"]
            elif item["type"] == "main" and main_name is None:
                main_name = item["name"]
            if bun_name and sauce_name and main_name:
                break

        if not (bun_name and sauce_name and main_name):
            pytest.fail("Не удалось найти все необходимые типы ингредиентов (булка, соус, начинка).")

        return {"bun": bun_name, "sauce": sauce_name, "main": main_name}