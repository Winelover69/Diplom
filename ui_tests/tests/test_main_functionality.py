import pytest
import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.order_feed_page import OrderFeedPage

@allure.epic("UI Stellar Burgers")
@allure.feature("Main Functionality")
class TestMainFunctionality:

    @allure.title("Переход по клику на «Конструктор»")
    @allure.description("Проверяет, что при клике на 'Конструктор' происходит переход на главную страницу с конструктором.")
    def test_navigate_to_constructor(self, driver):
        main_page = MainPage(driver)
        main_page.open("/feed") # Сначала переходим на другую страницу
        main_page.click_constructor_button()
        assert driver.current_url == main_page.base_url + "/"
        assert main_page.find_element(main_page.locators.BURGER_CONSTRUCTOR_TITLE).is_displayed()

    @allure.title("Переход по клику на раздел «Лента заказов»")
    @allure.description("Проверяет, что при клике на 'Лента заказов' происходит переход на соответствующую страницу.")
    def test_navigate_to_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.go_to_main_page() # Начинаем с главной
        main_page.click_order_feed_button()
        assert driver.current_url == main_page.base_url + "/feed"
        order_feed_page = OrderFeedPage(driver)
        assert order_feed_page.find_element(order_feed_page.locators.ORDER_FEED_TITLE).is_displayed()

    @allure.title("Если кликнуть на ингредиент, появится всплывающее окно с деталями")
    @allure.description("Проверяет открытие модального окна с деталями ингредиента по клику.")
    def test_ingredient_details_modal_opens(self, driver, get_some_ingredients_names):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        ingredient_name = get_some_ingredients_names["bun"] # Возьмем название булки
        main_page.click_ingredient(ingredient_name)
        assert main_page.is_ingredient_details_modal_displayed()

    @allure.title("Всплывающее окно закрывается кликом по крестику")
    @allure.description("Проверяет закрытие модального окна деталей ингредиента по клику на крестик.")
    def test_ingredient_details_modal_closes(self, driver, get_some_ingredients_names):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        ingredient_name = get_some_ingredients_names["sauce"] # Возьмем название соуса
        main_page.click_ingredient(ingredient_name)
        assert main_page.is_ingredient_details_modal_displayed()
        main_page.close_modal()
        assert not main_page.is_ingredient_details_modal_displayed()

    @allure.title("При добавлении ингредиента в заказ счётчик этого ингредиента увеличивается")
    @allure.description("Проверяет, что счетчик ингредиента увеличивается после его добавления в конструктор.")
    def test_ingredient_counter_increases_on_add(self, driver, get_some_ingredients_names):
        main_page = MainPage(driver)
        main_page.go_to_main_page()
        bun_name = get_some_ingredients_names["bun"]
        sauce_name = get_some_ingredients_names["sauce"]
        main_name = get_some_ingredients_names["main"]

        # Проверяем для булки
        initial_bun_counter = main_page.get_ingredient_counter_value(bun_name)
        main_page.add_ingredient_to_burger(bun_name)
        updated_bun_counter = main_page.get_ingredient_counter_value(bun_name)
        assert updated_bun_counter == initial_bun_counter + 2 # Булка добавляется сразу в двух экземплярах (верх и низ)

        # Проверяем для соуса
        initial_sauce_counter = main_page.get_ingredient_counter_value(sauce_name)
        main_page.add_ingredient_to_burger(sauce_name)
        updated_sauce_counter = main_page.get_ingredient_counter_value(sauce_name)
        assert updated_sauce_counter == initial_sauce_counter + 1

        # Проверяем для начинки
        initial_main_counter = main_page.get_ingredient_counter_value(main_name)
        main_page.add_ingredient_to_burger(main_name)
        updated_main_counter = main_page.get_ingredient_counter_value(main_name)
        assert updated_main_counter == initial_main_counter + 1