import requests
import allure
from urls import Urls
from data import Messages
from helpers import CourierHelpers
from generators import generate_courier_payload as generate_courier_data


@allure.epic("Яндекс Самокат API")
@allure.feature("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    @allure.description("Проверяем, что курьер может авторизоваться после успешного создания. Ожидаем код 200 и наличие id.")
    def test_login_courier_success(self):
        # Создаём курьера
        courier_data = generate_courier_data()
        create_response = CourierHelpers.create_courier_with_payload(courier_data)
        assert create_response.status_code == 201, "Не удалось создать курьера для авторизации"

        # Авторизация
        with allure.step("Отправляем запрос на логин"):
            login_payload = {
                "login": courier_data["login"],
                "password": courier_data["password"]
            }
            response = requests.post(Urls.LOGIN_COURIER, json=login_payload)

        assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"
        assert "id" in response.json(), f"В ответе нет id: {response.text}"

        # Удаляем курьера после теста
        courier_id = response.json().get("id")
        if courier_id:
            CourierHelpers.delete_courier(courier_id)

    @allure.title("Авторизация без логина")
    @allure.description("Проверяем, что при отсутствии логина запрос возвращает 400 и сообщение об ошибке.")
    def test_login_without_login(self):
        payload = {"password": "1234"}
        response = requests.post(Urls.LOGIN_COURIER, json=payload)

        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert Messages.COURIER_ID_REQUIRED in response.text, (
            f"Ожидали сообщение '{Messages.COURIER_ID_REQUIRED}', получили {response.text}"
        )

    @allure.title("Авторизация без пароля")
    @allure.description("Проверяем, что при пустом пароле запрос возвращает 400 и сообщение об ошибке.")
    def test_login_without_password(self):
        payload = {
            "login": "some_login",
            "password": ""  # отправляем пустое значение, чтобы избежать 504
        }
        response = requests.post(Urls.LOGIN_COURIER, json=payload)

        assert response.status_code == 400, f"Ожидали 400, получили {response.status_code}"
        assert Messages.COURIER_ID_REQUIRED in response.text, (
            f"Ожидали сообщение '{Messages.COURIER_ID_REQUIRED}', получили {response.text}"
        )

    @allure.title("Авторизация с неверным паролем")
    @allure.description("Проверяем, что при неправильном пароле возвращается 404 и сообщение об ошибке.")
    def test_login_with_wrong_password(self, create_and_delete_courier):
        courier_data = create_and_delete_courier

        payload = {
            "login": courier_data["login"],
            "password": "wrong_password"
        }
        response = requests.post(Urls.LOGIN_COURIER, json=payload)

        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"
        assert Messages.ACCOUNT_NOT_FOUND in response.text

    @allure.title("Авторизация под несуществующим курьером")
    @allure.description("Проверяем, что при логине несуществующего курьера возвращается 404 и сообщение об ошибке.")
    def test_login_nonexistent_courier(self):
        payload = {"login": "ghost_user", "password": "1234"}
        response = requests.post(Urls.LOGIN_COURIER, json=payload)

        assert response.status_code == 404, f"Ожидали 404, получили {response.status_code}"
        assert Messages.ACCOUNT_NOT_FOUND in response.text, (
            f"Ожидали сообщение '{Messages.ACCOUNT_NOT_FOUND}', получили {response.text}"
        )
