import requests
import allure
from urls import Urls
from data import Messages
from helpers import CourierHelpers
from generators import generate_courier_payload as generate_courier_data


@allure.epic("Яндекс Самокат API")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Создание нового курьера")
    @allure.description("Проверяем, что курьера можно успешно создать. Ожидаем код 201 и {'ok': true}.")
    def test_create_courier_success(self, create_and_delete_courier):
        """Создание нового курьера"""
        with allure.step("Проверяем, что курьер создан"):
            courier = create_and_delete_courier
            assert courier is not None, "Курьер должен быть успешно создан."

    @allure.title("Создание двух одинаковых курьеров запрещено")
    def test_create_duplicate_courier(self):
        """Проверяем, что нельзя создать курьера с тем же логином"""
        courier_data = generate_courier_data()

        with allure.step("Создаём первого курьера"):
            first = CourierHelpers.create_courier_with_payload(courier_data)
            assert first.status_code == 201, f"Ожидали 201, получили {first.status_code}"

        with allure.step("Пробуем создать дубликата"):
            duplicate = CourierHelpers.create_courier_with_payload(courier_data)
            assert duplicate.status_code == 409, f"Ожидали 409, получили {duplicate.status_code}"
            assert Messages.LOGIN_ALREADY_EXISTS in duplicate.text, "Сообщение об ошибке не совпадает"

        # Удаляем тестового курьера
        courier_id = CourierHelpers.get_courier_id(courier_data["login"], courier_data["password"])
        if courier_id:
            CourierHelpers.delete_courier(courier_id)

    @allure.title("Создание курьера без логина невозможно")
    def test_create_courier_without_login(self):
        """Проверяем, что без логина запрос не проходит"""
        payload = {"password": "1234", "firstName": "Ivan"}

        with allure.step("Отправляем POST без логина"):
            response = requests.post(Urls.CREATE_COURIER, json=payload)

        with allure.step("Проверяем код и сообщение об ошибке"):
            assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
            assert Messages.NOT_ENOUGH_DATA_FOR_CREATE in response.text

    @allure.title("Создание курьера без пароля невозможно")
    def test_create_courier_without_password(self):
        """Проверяем, что без пароля запрос не проходит"""
        payload = {"login": "no_pass_login", "firstName": "Petr"}

        with allure.step("Отправляем POST без пароля"):
            response = requests.post(Urls.CREATE_COURIER, json=payload)

        with allure.step("Проверяем код и сообщение об ошибке"):
            assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
            assert Messages.NOT_ENOUGH_DATA_FOR_CREATE in response.text

    @allure.title("Проверка успешного ответа: ok = true")
    def test_create_courier_returns_ok_true(self):
        """Проверяем, что успешное создание возвращает {'ok': true}"""
        courier_data = generate_courier_data()

        with allure.step("Создаём курьера"):
            response = CourierHelpers.create_courier_with_payload(courier_data)

            # Проверка кода ответа
            assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"

            # Проверка тела ответа
            expected = {"ok": True}
            actual = response.json()
            assert actual == expected, "Ожидали ответ {ok: True}, получили другой"

        # Удаляем тестового курьера после проверки
        courier_id = CourierHelpers.get_courier_id(courier_data["login"], courier_data["password"])
        if courier_id:
            CourierHelpers.delete_courier(courier_id)
