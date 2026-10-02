import random
import string

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def make_courier_payload():
    return {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(),
    }
