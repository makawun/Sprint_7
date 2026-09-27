import requests
import random
import string

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))


def delete_courier_by_credentials(base_url, login, password):
    login_response = requests.post(
        f"{base_url}/courier/login",
        data={"login": login, "password": password},
    )
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f"{base_url}/courier/{courier_id}")