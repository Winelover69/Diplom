import pytest
import allure
from api.client import ApiClient
from data.test_data import generate_random_email, generate_random_password, generate_random_name

@allure.epic("API Stellar Burgers")
@allure.feature("User Creation")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    @allure.description("Проверяет успешное создание пользователя с уникальными данными.")
    def test_create_unique_user_success(self, api_client, random_user_data):
        with allure.step("Отправка запроса на регистрацию"):
            response = api_client.register_user(
                random_user_data["email"],
                random_user_data["password"],
                random_user_data["name"]
            )
        with allure.step("Проверка ответа"):
            assert response.status_code == 200
            assert response.json()["success"] is True
            assert "accessToken" in response.json()
            assert "refreshToken" in response.json()
            assert response.json()["user"]["email"] == random_user_data["email"]
            assert response.json()["user"]["name"] == random_user_data["name"]
        with allure.step("Очистка: удаление созданного пользователя"):
            api_client.delete_user(response.json()["accessToken"])

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description("Проверяет, что нельзя создать пользователя с уже существующим email.")
    def test_create_existing_user_fails(self, api_client, registered_user):
        email, password, name, _ = registered_user # Пользователь уже зарегистрирован фикстурой
        with allure.step("Попытка повторной регистрации с тем же email"):
            response = api_client.register_user(email, password, name)
        with allure.step("Проверка ответа об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == "User already exists"

    @allure.title("Создание пользователя без заполнения обязательного поля")
    @allure.description("Проверяет, что регистрация невозможна без одного из обязательных полей (email, password, name).")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_required_field_fails(self, api_client, random_user_data, missing_field):
        user_data_copy = random_user_data.copy()
        user_data_copy.pop(missing_field) # Удаляем одно из обязательных полей

        with allure.step(f"Попытка регистрации без поля: {missing_field}"):
            response = api_client.register_user(
                email=user_data_copy.get("email"),
                password=user_data_copy.get("password"),
                name=user_data_copy.get("name")
            )
        with allure.step("Проверка ответа об ошибке"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == "Email, password and name are required fields"