import pytest
import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

@allure.epic("UI Stellar Burgers")
@allure.feature("Order Feed")
class TestOrderFeed:

    @allure.title("При создании нового заказа счётчик «Выполнено за всё время» увеличивается")
    @allure.description("Проверяет, что счетчик 'Выполнено за всё время' на странице Ленты заказов увеличивается после оформления нового заказа.")
    def test_total_orders_counter_increases(self, driver, registered_user_for_ui, get_some_ingredients_names):
        email, password, _, _ = registered_user_for_ui
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver)

        # 1. Логинимся
        main_page.go_to_main_page()
        main_page.click_login_on_main_page_button()
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_login_button()
        main_page.go_to_main_page() # Убеждаемся, что мы на главной после логина

        # 2. Получаем начальное значение счетчика "Выполнено за всё время"
        main_page.click_order_feed_button() # Переходим в ленту заказов
        initial_total_orders = order_feed_page.get_total_orders_counter()
        order_feed_page.click_constructor_button() # Возвращаемся в конструктор

        # 3. Создаем заказ
        main_page.add_ingredient_to_burger(get_some_ingredients_names["bun"])
        main_page.add_ingredient_to_burger(get_some_ingredients_names["sauce"])
        main_page.click_order_button()

        # 4. Получаем номер заказа и закрываем модальное окно
        order_number = main_page.get_order_number_from_modal()
        main_page.close_modal()

        # 5. Снова переходим в Ленту заказов и проверяем счетчик
        main_page.click_order_feed_button()
        updated_total_orders = order_feed_page.get_total_orders_counter()
        assert updated_total_orders == initial_total_orders + 1, "Счетчик 'Выполнено за всё время' не увеличился."
        # Проверяем, что номер заказа появился в общей ленте
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
            (By.XPATH, f"//ul[contains(@class, 'OrderFeed_list__')]//p[text()='#{order_number}']")
        ))


    @allure.title("При создании нового заказа счётчик «Выполнено за сегодня» увеличивается")
    @allure.description("Проверяет, что счетчик 'Выполнено за сегодня' на странице Ленты заказов увеличивается после оформления нового заказа.")
    def test_today_orders_counter_increases(self, driver, registered_user_for_ui, get_some_ingredients_names):
        email, password, _, _ = registered_user_for_ui
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver)

        # 1. Логинимся
        main_page.go_to_main_page()
        main_page.click_login_on_main_page_button()
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_login_button()
        main_page.go_to_main_page()

        # 2. Получаем начальное значение счетчика "Выполнено за сегодня"
        main_page.click_order_feed_button()
        initial_today_orders = order_feed_page.get_today_orders_counter()
        order_feed_page.click_constructor_button()

        # 3. Создаем заказ
        main_page.add_ingredient_to_burger(get_some_ingredients_names["bun"])
        main_page.add_ingredient_to_burger(get_some_ingredients_names["main"])
        main_page.click_order_button()

        # 4. Получаем номер заказа и закрываем модальное окно
        order_number = main_page.get_order_number_from_modal()
        main_page.close_modal()

        # 5. Снова переходим в Ленту заказов и проверяем счетчик
        main_page.click_order_feed_button()
        updated_today_orders = order_feed_page.get_today_orders_counter()
        assert updated_today_orders == initial_today_orders + 1, "Счетчик 'Выполнено за сегодня' не увеличился."

    @allure.title("После оформления заказа его номер появляется в разделе «В работе»")
    @allure.description("Проверяет, что номер только что оформленного заказа отображается в списке заказов 'В работе' на странице Ленты заказов.")
    def test_order_number_appears_in_in_progress_section(self, driver, registered_user_for_ui, get_some_ingredients_names):
        email, password, _, _ = registered_user_for_ui
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        order_feed_page = OrderFeedPage(driver)

        # 1. Логинимся
        main_page.go_to_main_page()
        main_page.click_login_on_main_page_button()
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_login_button()
        main_page.go_to_main_page()

        # 2. Создаем заказ
        main_page.add_ingredient_to_burger(get_some_ingredients_names["bun"])
        main_page.add_ingredient_to_burger(get_some_ingredients_names["sauce"])
        main_page.add_ingredient_to_burger(get_some_ingredients_names["main"])
        main_page.click_order_button()

        # 3. Получаем номер заказа и закрываем модальное окно
        order_number = main_page.get_order_number_from_modal()
        main_page.close_modal()

        # 4. Переходим в Ленту заказов
        main_page.click_order_feed_button()

        # 5. Проверяем, что номер заказа появился в разделе "В работе"
        # Для этого нужно дождаться появления заказа в ленте
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.XPATH, f"//ul[contains(@class, 'OrderFeed_list__')]//p[text()='#{order_number}']"))
        )
        orders_in_progress = order_feed_page.get_orders_in_progress_numbers()
        assert order_number in orders_in_progress, f"Номер заказа #{order_number} не найден в списке 'В работе'."