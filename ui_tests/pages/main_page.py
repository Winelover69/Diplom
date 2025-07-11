from pages.base_page import BasePage
from utils.locators import MainPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import allure

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/" # Относительный путь к главной странице

    @allure.step("Переход на главную страницу")
    def go_to_main_page(self):
        self.open(self.url)
        self.wait_for_visibility(MainPageLocators.BURGER_CONSTRUCTOR_TITLE)

    @allure.step("Клик по кнопке 'Конструктор'")
    def click_constructor_button(self):
        self.click_element(MainPageLocators.CONSTRUCTOR_BUTTON)
        self.wait_for_url_change(self.base_url + self.url)

    @allure.step("Клик по кнопке 'Лента заказов'")
    def click_order_feed_button(self):
        self.click_element(MainPageLocators.ORDER_FEED_BUTTON)
        self.wait_for_url_change("/feed")

    @allure.step("Клик по кнопке 'Личный Кабинет'")
    def click_profile_button(self):
        self.click_element(MainPageLocators.PROFILE_BUTTON)
        self.wait_for_url_change("/login") # Ведет на страницу логина, если не авторизован

    @allure.step("Клик по кнопке 'Войти в аккаунт' на главной странице")
    def click_login_on_main_page_button(self):
        self.click_element(MainPageLocators.LOGIN_BUTTON_ON_MAIN_PAGE)
        self.wait_for_url_change("/login")

    @allure.step("Клик по ингредиенту: {ingredient_name}")
    def click_ingredient(self, ingredient_name):
        self.click_element(MainPageLocators.get_ingredient_card_locator(ingredient_name))
        self.wait_for_visibility(MainPageLocators.INGREDIENT_DETAILS_MODAL_TITLE)

    @allure.step("Проверка отображения модального окна деталей ингредиента")
    def is_ingredient_details_modal_displayed(self):
        try:
            return self.find_element(MainPageLocators.INGREDIENT_DETAILS_MODAL_TITLE).is_displayed()
        except:
            return False

    @allure.step("Закрытие модального окна")
    def close_modal(self):
        self.click_element(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.wait_for_element_to_be_invisible(MainPageLocators.INGREDIENT_DETAILS_MODAL_TITLE)

    @allure.step("Получение значения счетчика ингредиента: {ingredient_name}")
    def get_ingredient_counter_value(self, ingredient_name):
        counter_locator = MainPageLocators.get_ingredient_counter_locator(ingredient_name)
        # Если счетчика нет (0), element_located не найдет его, поэтому проверяем наличие
        try:
            counter_text = self.find_element(counter_locator, timeout=2).text
            return int(counter_text)
        except (TimeoutException, AssertionError): # Если элемент не найден или Assertion failed (наш find_element)
            return 0 # Значит, счетчик равен 0 или отсутствует

    @allure.step("Добавление ингредиента '{ingredient_name}' в бургер")
    def add_ingredient_to_burger(self, ingredient_name):
        source_locator = MainPageLocators.get_ingredient_card_locator(ingredient_name)
        target_locator = MainPageLocators.BURGER_BUILDER_DROP_AREA
        self.drag_and_drop(source_locator, target_locator)

    @allure.step("Клик по кнопке 'Оформить заказ'")
    def click_order_button(self):
        self.click_element(MainPageLocators.ORDER_BUTTON)
        self.wait_for_visibility(MainPageLocators.ORDER_NUMBER_MODAL_TEXT)

    @allure.step("Получение номера заказа из модального окна")
    def get_order_number_from_modal(self):
        return self.get_text(MainPageLocators.ORDER_NUMBER_DISPLAY)

    @allure.step("Ожидание исчезновения модального окна с номером заказа")
    def wait_for_order_modal_to_disappear(self):
        self.wait_for_element_to_be_invisible(MainPageLocators.ORDER_NUMBER_MODAL_TEXT)