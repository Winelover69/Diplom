import requests

class ApiClient:
    BASE_URL = "https://stellarburgers.nomoreparties.site"

    def register_user(self, email, password, name):
        payload = {"email": email, "password": password, "name": name}
        return requests.post(f"{self.BASE_URL}/api/auth/register", json=payload)

    def login_user(self, email, password):
        payload = {"email": email, "password": password}
        return requests.post(f"{self.BASE_URL}/api/auth/login", json=payload)

    def delete_user(self, token):
        headers = {"Authorization": f"Bearer {token}"}
        return requests.delete(f"{self.BASE_URL}/api/auth/user", headers=headers)

    def get_ingredients(self):
        return requests.get(f"{self.BASE_URL}/api/ingredients")