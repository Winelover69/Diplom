from pages.base_page import BasePage
from utils.locators import LoginPageLocators # Используем локаторы логина, так как регистрация часто рядом
from selenium.webdriver.common.by import By # Для новых локаторов, если они специфичны для регистрации
import allure

class RegisterPageLocators:
    # Локаторы для страницы регистрации
    REGISTER_TITLE = (By.XPATH, "//h2[text()='Регистрация']")
    NAME_INPUT = (By.XPATH, "//label[text()='Имя']/following-sibling::input")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    REGISTER_BUTTON = (By.XPATH, "//button[text()='Зарегистрироваться']")
    LOGIN_LINK = (By.XPATH, "//a[text()='Войти']")
    INVALID_PASSWORD_ERROR = (By.XPATH, "//p[text()='Некорректный пароль']")

class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/register"

    @allure.step("Переход на страницу регистрации")
    def go_to_register_page(self):
        self.open(self.url)
        self.wait_for_visibility(RegisterPageLocators.REGISTER_TITLE)

    @allure.step("Ввод имени: {name}")
    def enter_name(self, name):
        self.find_element(RegisterPageLocators.NAME_INPUT).send_keys(name)

    @allure.step("Ввод Email: {email}")
    def enter_email(self, email):
        self.find_element(RegisterPageLocators.EMAIL_INPUT).send_keys(email)

    @allure.step("Ввод пароля")
    def enter_password(self, password):
        self.find_element(RegisterPageLocators.PASSWORD_INPUT).send_keys(password)

    @allure.step("Клик по кнопке 'Зарегистрироваться'")
    def click_register_button(self):
        self.click_element(RegisterPageLocators.REGISTER_BUTTON)
        # После успешной регистрации ожидаем редирект на страницу логина
        self.wait_for_url_change("/login")

    @allure.step("Проверка отображения ошибки 'Некорректный пароль'")
    def is_invalid_password_error_displayed(self):
        try:
            return self.find_element(RegisterPageLocators.INVALID_PASSWORD_ERROR).is_displayed()
        except:
            return False

    @allure.step("Клик по ссылке 'Войти'")
    def click_login_link(self):
        self.click_element(RegisterPageLocators.LOGIN_LINK)
        self.wait_for_url_change("/login")