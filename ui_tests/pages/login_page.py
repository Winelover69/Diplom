from pages.base_page import BasePage
from utils.locators import LoginPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/login"

    @allure.step("Переход на страницу логина")
    def go_to_login_page(self):
        self.open(self.url)
        self.wait_for_visibility(LoginPageLocators.LOGIN_TITLE)

    @allure.step("Ввод Email: {email}")
    def enter_email(self, email):
        self.find_element(LoginPageLocators.EMAIL_INPUT).send_keys(email)

    @allure.step("Ввод пароля")
    def enter_password(self, password):
        self.find_element(LoginPageLocators.PASSWORD_INPUT).send_keys(password)

    @allure.step("Клик по кнопке 'Войти'")
    def click_login_button(self):
        self.click_element(LoginPageLocators.LOGIN_BUTTON)
        # Ожидаем редирект на главную страницу или другую страницу после логина
        self.wait_for_url_change("/") # После успешного логина должен быть редирект на главную