import allure
import pytest

from api import create_courier, login_courier, delete_courier
from constants import (
    ERROR_LOGIN_ALREADY_USED,
    ERROR_NOT_ENOUGH_DATA_CREATE,
)


@allure.epic("API Яндекс.Самокат")
@allure.feature("Управление курьерами")
class TestCreateCourier:
    @allure.story("Создание курьера")
    @allure.title("Успешное создание курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier_success(self, courier_payload):
        with allure.step("Отправить POST-запрос на создание курьера"):
            response = create_courier(courier_payload)
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
            login_response = login_courier(
                courier_payload["login"],
                courier_payload["password"],
            )
            courier_id = login_response.json()["id"]
            delete_courier(courier_id)

    @allure.story("Создание курьера")
    @allure.title("Попытка создать дубликат курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_duplicate_courier_error(self, created_courier):
        with allure.step("Повторно отправить POST с данными существующего курьера"):
            response = create_courier(created_courier)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 409"):
            assert response.status_code == 409, \
                f"Ожидался 409, получен {response.status_code}: {response.text}"

        with allure.step("Проверить конкретный текст ошибки о дубликате логина"):
            assert response.json()["message"] == ERROR_LOGIN_ALREADY_USED, \
                f"Ожидалось '{ERROR_LOGIN_ALREADY_USED}', " \
                f"получено '{response.json().get('message')}'"

    @allure.story("Создание курьера")
    @allure.title("Создание без обязательного поля: {missing_field}")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_required_field(self, courier_payload, missing_field):
        with allure.step(f"Убрать обязательное поле '{missing_field}' из payload"):
            payload = courier_payload.copy()
            del payload[missing_field]

        with allure.step(f"Отправить POST-запрос без поля '{missing_field}'"):
            response = create_courier(payload)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 400"):
            assert response.status_code == 400, \
                f"Без поля '{missing_field}': ожидался 400, получен " \
                f"{response.status_code}: {response.text}"

        with allure.step("Проверить конкретный текст ошибки о нехватке данных"):
            assert response.json()["message"] == ERROR_NOT_ENOUGH_DATA_CREATE, \
                f"Ожидалось '{ERROR_NOT_ENOUGH_DATA_CREATE}', " \
                f"получено '{response.json().get('message')}'"

 