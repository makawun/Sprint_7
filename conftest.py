import pytest
import requests
from constants import BASE_URL
from helpers import generate_random_string, delete_courier_by_credentials


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def courier_payload():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }

@pytest.fixture
def created_courier(base_url, courier_payload):
    response = requests.post(f"{base_url}/courier", data=courier_payload)
    assert response.status_code == 201, \
        f"Фикстура не смогла создать курьера: {response.status_code} {response.text}"

    yield courier_payload

    delete_courier_by_credentials(
        base_url,
        courier_payload["login"],
        courier_payload["password"],
    )

@pytest.fixture
def login_url(base_url):
    return f"{base_url}/courier/login"


def login_courier(base_url, login, password):
    return requests.post(
        f"{base_url}/courier/login",
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


def cancel_order(base_url, track):
    requests.put(f"{base_url}/orders/cancel", params={"track": track})

@pytest.fixture
def created_order(base_url, order_payload):
    response = requests.post(f"{base_url}/orders", json=order_payload)
    assert response.status_code == 201, \
        f"Фикстура не смогла создать заказ: {response.status_code} {response.text}"

    track = response.json()["track"]
    yield track

    requests.put(f"{base_url}/orders/cancel", params={"track": track})