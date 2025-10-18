import requests
from urls import Urls
from generators import generate_courier_payload

class CourierHelpers:
    @staticmethod
    def create_courier():
        """
        Создаёт курьера с уникальными данными.
        Возвращает (response, payload)
        """
        payload = generate_courier_payload()
        response = requests.post(Urls.CREATE_COURIER, data=payload)
        return response, payload

    @staticmethod
    def create_courier_with_payload(payload: dict):
        """Создаёт курьера с переданным payload и возвращает response"""
        return requests.post(Urls.CREATE_COURIER, data=payload)

    @staticmethod
    def get_courier_id(login: str, password: str):
        """
        Пытается залогинить курьера и вернуть id (если авторизация успешна).
        Возвращает None при неуспехе.
        """
        response = requests.post(Urls.LOGIN_COURIER, data={"login": login, "password": password})
        if response.status_code == 200:
            try:
                return response.json().get("id")
            except Exception:
                return None
        return None

    @staticmethod
    def delete_courier(courier_id):
        """Удаляет курьера по id. Возвращает response."""
        if courier_id is None:
            return None
        return requests.delete(f"{Urls.DELETE_COURIER}/{courier_id}")
