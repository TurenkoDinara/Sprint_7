import requests
import allure
from urls import Urls
from data import Messages, CourierData
from helpers import CourierHelpers
from generators import generate_courier_payload as generate_courier_data


@allure.epic("Яндекс Самокат API")
@allure.feature("Создание курьера")
class TestCreateCourier:

    @allure.title("Создание нового курьера")
    @allure.description("Проверяем, что курьера можно успешно создать. Ожидаем код 201 и {'ok': true}.")
    def test_create_courier_success(self, delete_courier_after_test):
        """Создание нового курьера"""
        with allure.step("Формируем данные курьера"):
            courier_data = generate_courier_data()

        with allure.step("Отправляем запрос на создание курьера"):
            response = requests.post(Urls.CREATE_COURIER, json=courier_data)
            assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"

        with allure.step("Проверяем тело ответа"):
            expected = {"ok": True}
            actual = response.json()
            assert actual == expected, f"Ожидали {expected}, получили {actual}"

        # передаём курьера в фикстуру для удаления после теста
        delete_courier_after_test.append(courier_data)

    @allure.title("Создание двух одинаковых курьеров запрещено")
    @allure.description(
        "Проверяем, что нельзя создать курьера с тем же логином. Ожидаем 409 и сообщение 'Этот логин уже используется'.")
    def test_create_duplicate_courier(self, create_and_delete_courier):
        """Создание дубликата курьера — проверка, что API возвращает 409"""
        courier_data = create_and_delete_courier

        with allure.step("Пробуем создать курьера с тем же логином"):
            duplicate_response = CourierHelpers.create_courier_with_payload(courier_data)

        with allure.step("Проверяем, что создание дубликата запрещено"):
            assert duplicate_response.status_code == 409, (
                f"Ожидали код 409, получили {duplicate_response.status_code}. "
                f"Ответ: {duplicate_response.text}"
            )
            assert "Этот логин уже используется" in duplicate_response.text, (
                "Сообщение об ошибке должно содержать 'Этот логин уже используется'"
            )

    @allure.title("Создание курьера без логина невозможно")
    def test_create_courier_without_login(self):
        """Проверяем, что без логина запрос не проходит"""
        with allure.step("Отправляем POST без логина"):
            response = requests.post(Urls.CREATE_COURIER, json=CourierData.WITHOUT_LOGIN)

        with allure.step("Проверяем код и сообщение об ошибке"):
            assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
            assert Messages.NOT_ENOUGH_DATA_FOR_CREATE in response.text

    @allure.title("Создание курьера без пароля невозможно")
    def test_create_courier_without_password(self):
        """Проверяем, что без пароля запрос не проходит"""
        with allure.step("Отправляем POST без пароля"):
            response = requests.post(Urls.CREATE_COURIER, json=CourierData.WITHOUT_PASSWORD)

        with allure.step("Проверяем код и сообщение об ошибке"):
            assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
            assert Messages.NOT_ENOUGH_DATA_FOR_CREATE in response.text
            response = requests.post(Urls.CREATE_COURIER, json=CourierData.WITHOUT_PASSWORD)

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
