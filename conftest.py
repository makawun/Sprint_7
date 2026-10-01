import pytest

from api import (
    create_courier,
    create_order,
    cancel_order,
    delete_courier_by_credentials,
)
from helpers import generate_random_string


@pytest.fixture
def courier_payload():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }


@pytest.fixture
def created_courier(courier_payload):
    response = create_courier(courier_payload)
    if response.status_code != 201:
        pytest.fail(
            f"Не удалось создать курьера (предусловие): "
            f"{response.status_code} {response.text}"
        )

    yield courier_payload

    delete_courier_by_credentials(
        courier_payload["login"],
        courier_payload["password"],
    )

@pytest.fixture
def courier_with_cleanup(courier_payload):
    yield courier_payload

    delete_courier_by_credentials(
        courier_payload["login"],
        courier_payload["password"],
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


@pytest.fixture
def created_order(order_payload):
    response = create_order(order_payload)
    if response.status_code != 201:
        pytest.fail(
            f"Не удалось создать заказ (предусловие): "
            f"{response.status_code} {response.text}"
        )

    track = response.json()["track"]
    yield track

    cancel_order(track)