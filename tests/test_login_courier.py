import allure
import pytest
import requests

from helpers import generate_random_string
from urls import BASE_URL


@allure.epic("API Яндекс.Самокат")
@allure.feature("Управление курьерами")
class TestLoginCourier:
    @allure.story("Авторизация курьера")
    @allure.title("Успешная авторизация курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_courier_success(self, created_courier):
        with allure.step("Отправить POST-запрос на логин курьера"):
            response = requests.post(
                f"{BASE_URL}/courier/login",
                data={
                    "login": created_courier["login"],
                    "password": created_courier["password"],
                },
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
            response = requests.post(
                f"{BASE_URL}/courier/login",
                data={
                    "login": created_courier["login"],
                    "password": created_courier["password"],
                },
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
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400, \
                f"Пустое поле '{empty_field}': ожидался 400, получен " \
                f"{response.status_code}: {response.text}"

    @allure.story("Авторизация курьера")
    @allure.title("Логин с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid_password(self, created_courier):
        with allure.step("Отправить логин с правильным login и неправильным password"):
            response = requests.post(
                f"{BASE_URL}/courier/login",
                data={
                    "login": created_courier["login"],
                    "password": generate_random_string(),  # другой пароль
                },
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}: {response.text}"

        with allure.step("Проверить наличие message в теле ошибки"):
            assert "message" in response.json()

    @allure.story("Авторизация курьера")
    @allure.title("Логин с неверным логином")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid_login(self, created_courier):
        with allure.step("Отправить логин с несуществующим login и правильным password"):
            response = requests.post(
                f"{BASE_URL}/courier/login",
                data={
                    "login": generate_random_string(),  # несуществующий логин
                    "password": created_courier["password"],
                },
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}: {response.text}"

        with allure.step("Проверить наличие message в теле ошибки"):
            assert "message" in response.json()

    @allure.story("Авторизация курьера")
    @allure.title("Логин под несуществующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_nonexistent_user(self):
        with allure.step("Сформировать данные несуществующего курьера"):
            payload = {
                "login": generate_random_string(),
                "password": generate_random_string(),
            }

        with allure.step("Отправить POST-запрос на логин"):
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
            allure.attach(
                str(payload),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 404"):
            assert response.status_code == 404, \
                f"Ожидался 404, получен {response.status_code}: {response.text}"

        with allure.step("Проверить наличие message в теле ошибки"):
            assert "message" in response.json(), \
                f"Ожидалось поле 'message', получено {response.json()}"

    @allure.story("Авторизация курьера")
    @allure.title("Сообщение об ошибке логина не пустое")
    @allure.severity(allure.severity_level.MINOR)
    def test_login_message_not_empty(self):
        with allure.step("Отправить логин под несуществующим пользователем"):
            payload = {
                "login": generate_random_string(),
                "password": generate_random_string(),
            }
            response = requests.post(f"{BASE_URL}/courier/login", data=payload)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 404"):
            assert response.status_code == 404

        with allure.step("Проверить, что message не пустое"):
            message = response.json().get("message", "")
            assert message, f"Пустое сообщение об ошибке: {response.json()}"


    @allure.story("Авторизация курьера")
    @allure.title("Логин без обязательного поля 'login' → 400")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_without_login_returns_400(self, created_courier):
        with allure.step("Убрать поле 'login' из payload"):
            payload = {
                "password": created_courier["password"],
            }
            allure.attach(
                str(payload),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Отправить POST-запрос без поля 'login'"):
            response = requests.post(
                f"{BASE_URL}/courier/login",
                data=payload,
                timeout=30,
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.TEXT,
            )

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400, \
                f"Без поля 'login': ожидался 400, получен " \
                f"{response.status_code}: {response.text}"

        with allure.step("Проверить наличие message в теле ошибки"):
            assert "message" in response.json(), \
                f"Ожидалось поле 'message', получено {response.json()}"

