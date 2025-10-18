class Urls:
    BASE = "https://qa-scooter.praktikum-services.ru/"

    """"Ручки"""
    CREATE_COURIER = f"{BASE}/api/v1/courier" #Ручка на создание курьера (POST)
    LOGIN_COURIER = f"{BASE}/api/v1/courier/login" #Ручка на проверку логина курьера в системе (POST)
    DELETE_COURIER = f"{BASE}/api/v1/courier/" #Ручка на удаления курьера, динамическая (DELETE)
    CREATE_ORDER = f"{BASE}/api/v1/orders" #Ручка на создание заказа (POST)
    GET_ORDER_LIST = f"{BASE}/api/v1/orders" #Ручка на получение списка заказов (GET)

