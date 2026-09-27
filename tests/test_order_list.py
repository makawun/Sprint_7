import allure
import requests


@allure.epic("API Яндекс.Самокат")
@allure.feature("Управление заказами")
class TestGetOrdersList:
    @allure.story("Список заказов")
    @allure.title("Ручка списка заказов возвращает 200")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_returns_200(self, base_url):
        with allure.step("Отправить GET-запрос на /orders"):
            response = requests.get(f"{base_url}/orders")
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200, \
                f"Ожидался 200, получен {response.status_code}: {response.text}"

    @allure.story("Список заказов")
    @allure.title("Тело ответа содержит список заказов в ключе 'orders'")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_orders_body_contains_orders_list(self, base_url):
        with allure.step("Отправить GET-запрос на /orders"):
            response = requests.get(f"{base_url}/orders")
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверить код ответа 200"):
            assert response.status_code == 200

        with allure.step("Проверить наличие ключа 'orders' в теле ответа"):
            body = response.json()
            assert "orders" in body, \
                f"Ожидался ключ 'orders' в теле ответа, получено: {body}"

        with allure.step("Проверить, что 'orders' — список"):
            assert isinstance(body["orders"], list), \
                f"'orders' должен быть списком, получен {type(body['orders'])}"