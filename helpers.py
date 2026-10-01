import requests
import random
import string
from urls import BASE_URL

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def delete_courier_by_credentials(login, password):
    login_response = requests.post(
        f"{BASE_URL}/courier/login",
        data={"login": login, "password": password},
    )
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{BASE_URL}/courier/{courier_id}")

def login_courier(login, password):
    return requests.post(
        f"{BASE_URL}/courier/login",
        data={"login": login, "password": password},
    )


def cancel_order(track):
    requests.put(f"{BASE_URL}/orders/cancel", params={"track": track})