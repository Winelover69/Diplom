from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://stellarburgers.nomoreparties.site"

    @allure.step("Открытие URL: {url}")
    def open(self, url=""):
        self.driver.get(self.base_url + url)

    @allure.step("Ожидание и поиск элемента по локатору: {locator}")
    def find_element(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))
        except (TimeoutException, NoSuchElementException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Элемент не найден по локатору {locator} за {timeout} секунд: {e}")

    @allure.step("Клик по элементу: {locator}")
    def click_element(self, locator, timeout=10):
        self.find_element(locator, timeout).click()

    @allure.step("Получение текста элемента по локатору: {locator}")
    def get_text(self, locator, timeout=10):
        return self.find_element(locator, timeout).text

    @allure.step("Ожидание, пока элемент станет видимым: {locator}")
    def wait_for_visibility(self, locator, timeout=10):
        try:
            return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except (TimeoutException, NoSuchElementException) as e:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"Элемент не стал видимым по локатору {locator} за {timeout} секунд: {e}")

    @allure.step("Проверка отсутствия элемента: {locator}")
    def wait_for_element_to_be_invisible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
            return True
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            return False # Элемент остался видимым

    @allure.step("Выполнение drag-and-drop от {source_locator} к {target_locator}")
    def drag_and_drop(self, source_locator, target_locator):
        source_element = self.find_element(source_locator)
        target_element = self.find_element(target_locator)
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source_element, target_element).perform()

    @allure.step("Получение текущего URL")
    def get_current_url(self):
        return self.driver.current_url

    @allure.step("Ожидание изменения URL на {expected_url_part}")
    def wait_for_url_change(self, expected_url_part, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(EC.url_contains(expected_url_part))
        except TimeoutException:
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            raise AssertionError(f"URL не изменился на '{expected_url_part}' за {timeout} секунд. Текущий URL: {self.driver.current_url}")