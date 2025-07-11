import requests

class ApiClient:
    BASE_URL = "https://stellarburgers.nomoreparties.site"

    def register_user(self, email, password, name):
        """Регистрирует нового пользователя."""
        payload = {"email": email, "password": password, "name": name}
        return requests.post(f"{self.BASE_URL}/api/auth/register", json=payload)

    def login_user(self, email, password):
        """Выполняет вход пользователя."""
        payload = {"email": email, "password": password}
        return requests.post(f"{self.BASE_URL}/api/auth/login", json=payload)

    def delete_user(self, token):
        """Удаляет пользователя по токену авторизации."""
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(f"{self.BASE_URL}/api/auth/user", headers=headers)

    def create_order(self, ingredient_ids, token=None):
        """Создает новый заказ."""
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        payload = {"ingredients": ingredient_ids}
        return requests.post(f"{self.BASE_URL}/api/orders", json=payload, headers=headers)

    def get_ingredients(self):
        """Получает список всех доступных ингредиентов."""
        return requests.get(f"{self.BASE_URL}/api/ingredients")

    # Дополнительные методы API, если понадобятся для будущих тестов
    def get_user_orders(self, token):
        """Получает список заказов пользователя."""
        headers = {"Authorization": f"Bearer {token}"}
        return requests.get(f"{self.BASE_URL}/api/orders", headers=headers)

    def update_user_info(self, token, email=None, password=None, name=None):
        """Обновляет информацию о пользователе."""
        headers = {"Authorization": f"Bearer {token}"}
        payload = {}
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        if name:
            payload["name"] = name
        return requests.patch(f"{self.BASE_URL}/api/auth/user", json=payload, headers=headers)