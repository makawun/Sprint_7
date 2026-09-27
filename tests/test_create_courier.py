import allure
import pytest
import requests


@allure.epic("API Яндекс.Самокат")
@allure.feature("Управление курьерами")
class TestCreateCourier:
    @allure.story("Создание курьера")
    @allure.title("Успешное создание курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self, base_url, courier_payload):
        with allure.step("Отправить POST-запрос на создание курьера"):
            response = requests.post(f"{base_url}/courier", data=courier_payload)
            allure.attach(
                str(courier_payload),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 201"):
            assert response.status_code == 201, \
                f"Ожидался 201, получен {response.status_code}: {response.text}"

        with allure.step('Проверить тело ответа {"ok": true}'):
            assert response.json() == {"ok": True}, \
                f"Ожидался {{'ok': True}}, получен {response.json()}"

        with allure.step("Удалить созданного курьера"):
            login = requests.post(
                f"{base_url}/courier/login",
                data={
                    "login": courier_payload["login"],
                    "password": courier_payload["password"],
                },
            )
            if login.status_code == 200:
                requests.delete(f"{base_url}/courier/{login.json()['id']}")

    @allure.story("Создание курьера")
    @allure.title("Попытка создать дубликат курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_duplicate_courier_error(self, base_url, created_courier):
        with allure.step("Повторно отправить POST с данными существующего курьера"):
            response = requests.post(f"{base_url}/courier", data=created_courier)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 409"):
            assert response.status_code == 409, \
                f"Ожидался 409, получен {response.status_code}: {response.text}"

        with allure.step("Проверить наличие message в теле ошибки"):
            assert "message" in response.json(), \
                f"Ожидалось поле 'message', получено {response.json()}"

    @allure.story("Создание курьера")
    @allure.title("Создание без обязательного поля: {missing_field}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(
        self, base_url, courier_payload, missing_field
    ):
        with allure.step(f"Убрать обязательное поле '{missing_field}' из payload"):
            payload = courier_payload.copy()
            del payload[missing_field]

        with allure.step(f"Отправить POST-запрос без поля '{missing_field}'"):
            response = requests.post(f"{base_url}/courier", data=payload)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400, \
                f"Без поля '{missing_field}': ожидался 400, получен " \
                f"{response.status_code}: {response.text}"

        with allure.step("Проверить наличие message в теле ошибки"):
            assert "message" in response.json(), \
                f"Ожидалось поле 'message', получено {response.json()}"

    @allure.story("Создание курьера")
    @allure.title("Сообщение об ошибке дубликата не пустое")
    @allure.severity(allure.severity_level.MINOR)
    def test_duplicate_login_message_not_empty(self, base_url, created_courier):
        with allure.step("Повторно отправить POST с существующим логином"):
            response = requests.post(f"{base_url}/courier", data=created_courier)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 409"):
            assert response.status_code == 409

        with allure.step("Проверить, что message не пустое"):
            message = response.json().get("message", "")
            assert message, f"Пустое сообщение об ошибке: {response.json()}"