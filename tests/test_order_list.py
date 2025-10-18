import requests
import allure
from urls import Urls


@allure.epic("Яндекс Самокат API")
@allure.feature("Список заказов")
class TestGetOrdersList:

    @allure.title("Проверка получения списка заказов")
    @allure.description("Проверяем, что при запросе списка заказов возвращается статус 200 и тело содержит список 'orders'.")
    def test_get_orders_list(self):
        """Проверяем, что возвращается список заказов"""
        with allure.step("Отправляем GET-запрос на получение списка заказов"):
            response = requests.get(Urls.GET_ORDER_LIST)

        with allure.step("Проверяем успешный статус ответа"):
            assert response.status_code == 200, f"Ожидали 200, получили {response.status_code}"

        with allure.step("Проверяем, что тело содержит список заказов"):
            response_json = response.json()
            assert "orders" in response_json, "В ответе нет ключа 'orders'"
            assert isinstance(response_json["orders"], list), "Поле 'orders' должно быть списком"
