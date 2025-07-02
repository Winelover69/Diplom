import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import allure

@pytest.fixture(params=["chrome", "firefox"], scope="function")
def driver(request):
    """
    Фикстура для инициализации WebDriver.
    Запускает тесты в Chrome и Firefox.
    """
    driver = None
    if request.param == "chrome":
        with allure.step("Инициализация Chrome WebDriver"):
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service)
    elif request.param == "firefox":
        with allure.step("Инициализация Firefox WebDriver"):
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service)

    driver.maximize_window()
    yield driver
    with allure.step("Завершение работы WebDriver"):
        driver.quit()