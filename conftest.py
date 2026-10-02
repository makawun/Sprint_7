import pytest

from api import (
    create_courier,
    create_order,
    cancel_order,
    delete_courier_by_credentials,
)
from helpers import make_courier_payload


@pytest.fixture
def created_courier():
    payload = make_courier_payload()
    response = create_courier(payload)
    if response.status_code != 201:
        pytest.fail(
            f"Не удалось создать курьера (предусловие): "
            f"{response.status_code} {response.text}"
        )

    yield payload

    delete_courier_by_credentials(payload["login"], payload["password"])


@pytest.fixture
def created_order():
    from data import ORDER_PAYLOAD

    response = create_order(ORDER_PAYLOAD)
    if response.status_code != 201:
        pytest.fail(
            f"Не удалось создать заказ (предусловие): "
            f"{response.status_code} {response.text}"
        )

    track = response.json()["track"]
    yield track

    cancel_order(track)

@pytest.fixture
def courier_with_cleanup():
    payload = make_courier_payload()
    yield payload
    delete_courier_by_credentials(payload["login"], payload["password"])