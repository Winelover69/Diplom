import pytest
import allure
import logging
from api.client import ApiClient
from data.test_data import generate_random_email, generate_random_password, \
    generate_random_name

# Настройка логгера для conftest
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
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
    """
    email = random_user_data["email"]
    password = random_user_data["password"]
    name = random_user_data["name"]
    token = None  # Инициализируем токен как None

    with allure.step(f"Регистрация пользователя в фикстуре: {email}"):
        response = api_client.register_user(email, password, name)

        if response.status_code == 200 and response.json().get("success"):
            token = response.json().get("accessToken")
            logger.info(f"Пользователь {email} успешно зарегистрирован в фикстуре. Токен получен.")
        else:
            # Если регистрация не удалась, явно прерываем выполнение тестов через pytest.fail
            logger.error(
                f"Ошибка при регистрации пользователя {email} в фикстуре. Статус: {response.status_code}, Ответ: {response.text}")
            pytest.fail(
                f"Фикстура 'registered_user': Не удалось зарегистрировать пользователя через API. Ответ: {response.text}")

    # Убеждаемся, что токен был получен. Если нет, это проблема фикстуры, и тесты не должны продолжаться.
    if not token:
        pytest.fail(f"Фикстура 'registered_user': Токен не был получен после регистрации пользователя {email}.")

    yield email, password, name, token

    with allure.step(f"Удаление пользователя в фикстуре: {email}"):
        if token:
            response = api_client.delete_user(token)
            if response.status_code == 202 and response.json().get("success"):
                logger.info(f"Пользователь {email} успешно удален после теста.")
            else:
                logger.warning(
                    f"Не удалось удалить пользователя {email}. Статус: {response.status_code}, Ответ: {response.text}")
        else:
            logger.info(f"Токен для пользователя {email} не был получен в фикстуре, удаление пропущено.")


@pytest.fixture(scope="session")
def get_some_ingredients_ids(api_client):
    """
    Фикстура, получающая ID нескольких ингредиентов (булка, соус, начинка)
    для создания заказа. Выполняется один раз за тестовую сессию.
    Возвращает словарь с ID булки, соуса и начинки.
    """
    bun_id = None
    sauce_id = None
    main_id = None

    with allure.step("Получение ID ингредиентов через API"):
        response = api_client.get_ingredients()

        # ИСПРАВЛЕНИЕ: Завершение условия и проверка success
        if response.status_code != 200 or not response.json().get("success"):
            logger.error(f"Ошибка при получении ингредиентов. Статус: {response.status_code}, Ответ: {response.text}")
            pytest.fail(
                f"Фикстура 'get_some_ingredients_ids': Не удалось получить список ингредиентов через API. Ответ: {response.text}")

        ingredients = response.json().get("data", [])

        # Фильтруем ингредиенты по типу
        buns = [ing for ing in ingredients if ing.get("type") == "bun"]
        sauces = [ing for ing in ingredients if ing.get("type") == "sauce"]
        mains = [ing for ing in ingredients if ing.get("type") == "main"]

        # Получаем ID первого доступного ингредиента каждого типа
        if buns:
            bun_id = buns[0].get("_id")
        if sauces:
            sauce_id = sauces[0].get("_id")
        if mains:
            main_id = mains[0].get("_id")

        # Проверяем, что необходимые ингредиенты найдены. Если нет, фикстура должна упасть.
        if not all([bun_id, sauce_id, main_id]):
            missing_items = []
            if not bun_id: missing_items.append("булки")
            if not sauce_id: missing_items.append("соуса")
            if not main_id: missing_items.append("начинки")
            pytest.fail(
                f"Фикстура 'get_some_ingredients_ids': Не удалось найти все необходимые типы ингредиентов: {', '.join(missing_items)}.")

        logger.info(f"Получены ID ингредиентов: Булка={bun_id}, Соус={sauce_id}, Начинка={main_id}")

    return {"bun_id": bun_id, "sauce_id": sauce_id, "main_id": main_id}