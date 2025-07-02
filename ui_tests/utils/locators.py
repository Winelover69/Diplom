from selenium.webdriver.common.by import By

class BasePageLocators:
    # Общие локаторы, которые могут быть на многих страницах
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента заказов']")
    PROFILE_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")
    LOGIN_BUTTON_ON_MAIN_PAGE = (By.XPATH, "//button[text()='Войти в аккаунт']")
    MODAL_CLOSE_BUTTON = (By.XPATH, ".//*[contains(@class, 'Modal_modal__close_button')]")

class MainPageLocators(BasePageLocators):
    # Локаторы для главной страницы
    BURGER_CONSTRUCTOR_TITLE = (By.XPATH, "//h1[text()='Соберите бургер']")
    BUN_SECTION = (By.XPATH, "//span[text()='Булки']")
    SAUCE_SECTION = (By.XPATH, "//span[text()='Соусы']")
    FILLING_SECTION = (By.XPATH, "//span[text()='Начинки']")
    ANY_INGREDIENT_CARD = (By.XPATH, ".//li[contains(@class, 'BurgerIngredients_ingredient__')]") # Любая карточка ингредиента
    INGREDIENT_DETAILS_MODAL_TITLE = (By.XPATH, "//h2[text()='Детали ингредиента']")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_NUMBER_MODAL_TEXT = (By.XPATH, ".//h2[contains(@class, 'Modal_modal__title')]")
    ORDER_NUMBER_DISPLAY = (By.XPATH, ".//div[contains(@class, 'order-details_orderNumber__')]/p")
    BURGER_BUILDER_DROP_AREA = (By.XPATH, ".//div[contains(@class, 'BurgerConstructor_burger__')]")

    # Локатор для счетчика ингредиента (можно сделать динамическим)
    def get_ingredient_counter_locator(self, ingredient_name):
        return (By.XPATH, f"//p[text()='{ingredient_name}']/following-sibling::p[contains(@class, 'counter__num')]")

    # Локатор для конкретного ингредиента
    def get_ingredient_card_locator(self, ingredient_name):
        return (By.XPATH, f"//p[text()='{ingredient_name}']")

class LoginPageLocators:
    # Локаторы для страницы логина
    LOGIN_TITLE = (By.XPATH, "//h2[text()='Вход']")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::input")
    PASSWORD_INPUT = (By.XPATH, "//label[text()='Пароль']/following-sibling::input")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    REGISTER_LINK = (By.XPATH, "//a[text()='Зарегистрироваться']")

class OrderFeedPageLocators(BasePageLocators):
    # Локаторы для страницы "Лента заказов"
    ORDER_FEED_TITLE = (By.XPATH, "//h1[text()='Лента заказов']")
    TOTAL_ORDERS_COUNTER = (By.XPATH, ".//p[text()='Выполнено за всё время']/following-sibling::p")
    TODAY_ORDERS_COUNTER = (By.XPATH, ".//p[text()='Выполнено за сегодня']/following-sibling::p")
    ORDER_IN_PROGRESS_LIST = (By.XPATH, ".//ul[contains(@class, 'OrderFeed_list__')]")
    ANY_ORDER_IN_PROGRESS = (By.XPATH, ".//ul[contains(@class, 'OrderFeed_list__')]/li[1]//p[contains(@class, 'OrderFeed_number')]") # Первый заказ в списке