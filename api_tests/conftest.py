import pytest
import allure
import logging
from api.client import ApiClient  # Убедитесь, что путь к api.client корректен
from data.test_data import generate_random_email, generate_random_password, \
    generate_random_name  # Убедитесь, что путь к data.test_data корректен
import time  # Оставлен на случай, если всё же потребуется, но с комментарием.

# Настройка логгера для conftest
logger = logging.getLogger(__name__)
# Установите уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# INFO - хороший уровень для обычных сообщений о выполнении фикстур.
logger.setLevel(logging.INFO)
# Добавляем обработчик, чтобы логи выводились в консоль
handler = logging.StreamHandler()
# Формат вывода логов: время - имя логгера - уровень - сообщение
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# Проверяем, чтобы обработчик не добавлялся несколько раз при повторных запусках тестов
if not logger.handlers:
    logger.addHandler(handler)


@pytest.fixture(scope="session")
def api_client():
    """Фикстура, предоставляющая экземпляр ApiClient для всех тестов в рамках сессии."""
    return ApiClient()


@pytest.fixture
def random_user_data():
    """Фикстура, генерирующая случайные данные для регистрации пользователя."""
    email = generate_random_email()
    password = generate_random_password()
    name = generate_random_name()
    logger.info(f"Сгенерированы случайные данные пользователя: email={email}, name={name}")
    return {"email": email, "password": password, "name": name}


@pytest.fixture
def registered_user(api_client, random_user_data):
    """
    Фикстура, регистрирующая пользователя перед тестом и удаляющая его после.
    Возвращает данные пользователя и токен доступа.
    Проверки на успешность регистрации (status_code 200) должны быть в самом тестовом методе,
    который использует эту фикстуру для проверки регистрации.
    Здесь мы лишь убеждаемся, что фикстура смогла получить токен для последующих действий.
    """
    email = random_user_data["email"]
    password = random_user_data["password"]
    name = random_user_data["name"]
    token = None  # Инициализируем токен как None

    with allure.step(f"Регистрация пользователя в фикстуре: {email}"):
        response = api_client.register_user(email, password, name)

        # В фикстуре не делаем assert 200, чтобы не "скрывать" падение тестов.
        # Если регистрация не удалась, это будет видно по отсутствию токена.
        if response.status_code == 200:
            token = response.json().get("accessToken")
            logger.info(f"Пользователь {email} успешно зарегистрирован в фикстуре. Токен получен.")
        else:
            # Если регистрация не удалась, логируем ошибку и используем pytest.fail
            # чтобы явно показать, что фикстура не смогла подготовить данные.
            logger.error(
                f"Ошибка при регистрации пользователя {email} в фикстуре. Статус: {response.status_code}, Ответ: {response.text}")
            pytest.fail(f"Фикстура: Не удалось зарегистрировать пользователя через API. Ответ: {response.text}")

    yield email, password, name, token

    with allure.step(f"Удаление пользователя в фикстуре: {email}"):
        if token:
            response = api_client.delete_user(token)
            if response.status_code == 202:
                logger.info(f"Пользователь {email} успешно удален после теста.")
            else:
                logger.warning(
                    f"Не удалось удалить пользователя {email}. Статус: {response.status_code}, Ответ: {response.text}")
            # Не используем time.sleep(), если нет явной необходимости (например, жесткий rate limit, который не обходится polling'ом)
            # Если возникнут проблемы со слишком быстрыми запросами к API после удаления, можно вернуть с логированием.
        else:
            logger.info(f"Токен для пользователя {email} не был получен в фикстуре, удаление пропущено.")


@pytest.fixture(scope="session")
def get_some_ingredients_ids(api_client):
    """
    Фикстура, получающая ID нескольких ингредиентов (булка, соус, начинка)
    для создания заказа. Выполняется один раз за тестовую сессию.
    """
    with allure.step("Получение ID ингредиентов через API"):
        response = api_client.get_ingredients()

        # Здесь также: проверка в фикстуре только на критическую проблему.
        if response.status_code != 2