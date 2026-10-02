import requests
from urls import BASE_URL

def create_courier(payload):
    return requests.post(f"{BASE_URL}/courier", data=payload)


def login_courier(login, password):
    return requests.post(
        f"{BASE_URL}/courier/login",
        data={"login": login, "password": password},
    )


def delete_courier(courier_id):
    return requests.delete(f"{BASE_URL}/courier/{courier_id}")


def delete_courier_by_credentials(login, password):
    login_response = login_courier(login, password)
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            delete_courier(courier_id)


def create_order(payload):
    return requests.post(f"{BASE_URL}/orders", json=payload)


def get_orders():
    return requests.get(f"{BASE_URL}/orders")


def cancel_order(track):
    return requests.put(f"{BASE_URL}/orders/cancel", params={"track": track})