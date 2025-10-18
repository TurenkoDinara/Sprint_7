import requests
import random
import string
from urls import Urls

def _generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_courier_payload():
    """Генерирует payload для нового курьера"""
    return {
        "login": _generate_random_string(10),
        "password": _generate_random_string(10),
        "firstName": _generate_random_string(6)
    }

def register_new_courier_and_return_login_password():
    """
    Метод — регистрирует курьера и возвращает [login, password, firstName]
    Если регистрация не удалась — возвращает пустой список
    """
    payload = generate_courier_payload()
    response = requests.post(Urls.CREATE_COURIER, data=payload)
    if response.status_code == 201:
        return [payload["login"], payload["password"], payload["firstName"]]
    return []