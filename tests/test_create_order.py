import allure
import pytest
import requests

from conftest import cancel_order
from constants import COLOR_CASES
from urls import BASE_URL


@allure.epic("API Яндекс.Самокат")
@allure.feature("Управление заказами")
class TestCreateOrder:
    @allure.story("Создание заказа")
    @allure.title("Создание заказа с цветом: {color}")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("color", COLOR_CASES)
    def test_create_order_with_color_variations(self, order_payload, color):
        with allure.step(f"Сформировать payload с color={color}"):
            payload = order_payload.copy()
            if color is not None:
                payload["color"] = color
            # если color is None — поле color в запрос не добавляем вообще

            allure.attach(
                str(payload),
                name="Request Payload",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Отправить POST-запрос на создание заказа"):
            response = requests.post(f"{BASE_URL}/orders", json=payload)
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 201"):
            assert response.status_code == 201, \
                f"color={color}: ожидался 201, получен " \
                f"{response.status_code}: {response.text}"

        with allure.step("Проверить наличие ключа 'track' в теле ответа"):
            body = response.json()
            assert "track" in body, \
                f"color={color}: ожидался ключ 'track', получено {body}"

        with allure.step("Проверить, что 'track' — число"):
            assert isinstance(body["track"], int), \
                f"color={color}: track должен быть числом, " \
                f"получен {type(body['track'])}"

        with allure.step("Отменить созданный заказ"):
            cancel_order(BASE_URL, body["track"])