class Messages:

    # Сообщения об ошибках создания и работы с курьерами
    LOGIN_ALREADY_EXISTS = "Этот логин уже используется"
    NOT_ENOUGH_DATA_FOR_CREATE = "Недостаточно данных для создания учетной записи"
    COURIER_NOT_FOUND = "Курьера с таким id нет"
    COURIER_ID_REQUIRED = "Недостаточно данных для входа"
    ACCOUNT_NOT_FOUND = "Учетная запись не найдена"
    INVALID_INPUT_SYNTAX = "invalid input syntax"

    # Успешные сообщения
    OK_TRUE = '{"ok":true}'
    TRACK_FIELD = "track"
# data.py

class OrderData:
    BASE_ORDER = {
        "firstName": "Иван",
        "lastName": "Иванов",
        "address": "Москва, Тверская 1",
        "metroStation": 1,
        "phone": "+79999999999",
        "rentTime": 5,
        "deliveryDate": "2025-10-18",
        "comment": "Заказ самоката",
    }
