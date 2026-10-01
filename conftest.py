import pytest
import requests
from helpers import generate_random_string, delete_courier_by_credentials, cancel_order
from urls import BASE_URL

@pytest.fixture
def courier_payload():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }

@pytest.fixture
def created_courier(courier_payload):
    response = requests.post(f"{BASE_URL}/courier", data=courier_payload)
    if response.status_code != 201:
        pytest.fail(
            f"Не удалось создать курьера (предусловие): "
            f"{response.status_code} {response.text}"
        )

    yield courier_payload

    delete_courier_by_credentials(courier_payload["login"], courier_payload["password"],)

@pytest.fixture
def login_url():
    return f"{BASE_URL}/courier/login"


def login_courier(login, password):
    return requests.post(
        f"{BASE_URL}/courier/login",
        data={"login": login, "password": password},
    )

@pytest.fixture
def order_payload():
    return {
        "firstName": "Naruto",
        "lastName": "Uchiha",
        "address": "Konoha, 142 apt.",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": "2020-06-06",
        "comment": "Saske, come back to Konoha",
    }


def cancel_order(track):
    requests.put(f"{BASE_URL}/orders/cancel", params={"track": track})

@pytest.fixture
def created_order(order_payload):
    response = requests.post(f"{BASE_URL}/orders", json=order_payload)
    if response.status_code != 201:
        pytest.fail(
            f"Не удалось создать заказ (предусловие): "
            f"{response.status_code} {response.text}"
        )

    track = response.json()["track"]
    yield track

    requests.put(f"{BASE_URL}/orders/cancel", params={"track": track})