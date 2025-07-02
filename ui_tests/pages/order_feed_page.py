from pages.base_page import BasePage
from utils.locators import OrderFeedPageLocators
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import allure

class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "/feed"

    @allure.step("Переход на страницу 'Лента заказов'")
    def go_to_order_feed_page(self):
        self.open(self.url)
        self.wait_for_visibility(OrderFeedPageLocators.ORDER_FEED_TITLE)

    @allure.step("Получение значения счетчика 'Выполнено за всё время'")
    def get_total_orders_counter(self):
        return int(self.get_text(OrderFeedPageLocators.TOTAL_ORDERS_COUNTER))

    @allure.step("Получение значения счетчика 'Выполнено за сегодня'")
    def get_today_orders_counter(self):
        return int(self.get_text(OrderFeedPageLocators.TODAY_ORDERS_COUNTER))

    @allure.step("Получение списка номеров заказов в разделе 'В работе'")
    def get_orders_in_progress_numbers(self):
        # Ожидаем, что хотя бы один заказ появится в списке
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(OrderFeedPageLocators.ANY_ORDER_IN_PROGRESS)
        )
        # Находим все элементы, содержащие номера заказов в разделе "В работе"
        order_elements = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'OrderFeed_list__')]//li//p[contains(@class, 'OrderFeed_number')]")
        return [elem.text.replace("#", "") for elem in order_elements if elem.text.strip()] # Убираем # и пустые строки