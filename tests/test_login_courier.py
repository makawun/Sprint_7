import allure
import pytest

from api import login_courier
from helpers import generate_random_string
from constants import (
    ERROR_ACCOUNT_NOT_FOUND,
    ERROR_NOT_ENOUGH_DATA_LOGIN,
)


@allure.epic("API Яндекс.Самокат")
@allure.feature("Управление курьерами")
class TestLoginCourier:
    @allure.story("Авторизация курьера")
    @allure.title("Успешная авторизация курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_courier_success(self, created_courier):
        with allure.step("Отправить POST-запрос на логин курьера"):
            response = login_courier(
                created_courier["login"],
                created_courier["password"],
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}: {response.text}"

        with allure.step("Проверить наличие ключа 'id' в теле ответа"):
            body = response.json()
            assert "id" in body, f"Ожидался ключ 'id', получено {body}"

        with allure.step("Проверить, что 'id' — число"):
            assert isinstance(body["id"], int), \
                f"id должен быть числом, получен {type(body['id'])}"

    @allure.story("Авторизация курьера")
    @allure.title("Успешный логин возвращает только id")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_courier_returns_id(self, created_courier):
        with allure.step("Отправить POST-запрос на логин курьера"):
            response = login_courier(
                created_courier["login"],
                created_courier["password"],
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200

        with allure.step("Проверить, что тело ответа содержит только 'id'"):
            assert response.json().keys() == {"id"}, \
                f"Ожидался только ключ 'id', получено {response.json()}"

    @allure.story("Авторизация курьера")
    @allure.title("Логин с пустым обязательным полем: {empty_field}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("empty_field", ["login", "password"])
    def test_login_empty_required_field(self, created_courier, empty_field):
        with allure.step(f"Передать пустое значение в поле '{empty_field}'"):
            payload = {
                "login": created_courier["login"],
                "password": created_courier["password"],
            }
            payload[empty_field] = ""

        with allure.step(f"Отправить POST-запрос с пустым '{empty_field}'"):
            response = login_courier(payload["login"], payload["password"])
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400, \
                f"Пустое поле '{empty_field}': ожидался 400, получен " \
                f"{response.status_code}: {response.text}"

        with allure.step("Проверить конкретный текст ошибки о нехватке данных"):
            assert response.json()["message"] == ERROR_NOT_ENOUGH_DATA_LOGIN, \
                f"Ожидалось '{ERROR_NOT_ENOUGH_DATA_LOGIN}', " \
                f"получено '{response.json().get('message')}'"

    @allure.story("Авторизация курьера")
    @allure.title("Логин с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid_password(self, created_courier):
        with allure.step("Отправить логин с правильным login и неправильным password"):
            response = login_courier(
                created_courier["login"],
                generate_random_string(),
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить конкретный текст ошибки об отсутствии учётной записи"):
            assert response.json()["message"] == ERROR_ACCOUNT_NOT_FOUND, \
                f"Ожидалось '{ERROR_ACCOUNT_NOT_FOUND}', " \
                f"получено '{response.json().get('message')}'"

    @allure.story("Авторизация курьера")
    @allure.title("Логин с неверным логином")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid_login(self, created_courier):
        with allure.step("Отправить логин с несуществующим login и правильным password"):
            response = login_courier(
                generate_random_string(),
                created_courier["password"],
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить конкретный текст ошибки об отсутствии учётной записи"):
            assert response.json()["message"] == ERROR_ACCOUNT_NOT_FOUND, \
                f"Ожидалось '{ERROR_ACCOUNT_NOT_FOUND}', " \
                f"получено '{response.json().get('message')}'"

    @allure.story("Авторизация курьера")
    @allure.title("Логин под несуществующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_user(self):
        with allure.step("Сформировать данные несуществующего курьера"):
            login = generate_random_string()
            password = generate_random_string()

        with allure.step("Отправить POST-запрос на логин"):
            response = login_courier(login, password)
            allure.attach(
                f'{{"login": "{login}", "password": "{password}"}}',
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить конкретный текст ошибки об отсутствии учётной записи"):
            assert response.json()["message"] == ERROR_ACCOUNT_NOT_FOUND, \
                f"Ожидалось '{ERROR_ACCOUNT_NOT_FOUND}', " \
                f"получено '{response.json().get('message')}'"

    @allure.story("Авторизация курьера")
    @allure.title("Логин без обязательного поля 'login' - 400")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_without_login_returns_400(self, created_courier):
        with allure.step("Убрать поле 'login' из payload"):
            password = created_courier["password"]

        with allure.step("Отправить POST-запрос без поля 'login'"):
            response = login_courier("", password)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверить конкретный текст ошибки о нехватке данных"):
            assert response.json()["message"] == ERROR_NOT_ENOUGH_DATA_LOGIN, \
                f"Ожидалось '{ERROR_NOT_ENOUGH_DATA_LOGIN}', " \
                f"получено '{response.json().get('message')}'"
            