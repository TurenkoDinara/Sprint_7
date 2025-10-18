import pytest
import requests
import allure
from urls import Urls
from data import OrderData


@allure.epic("Яндекс Самокат API")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с различными вариантами цветов")
    @allure.description("Проверяем, что заказ можно создать с цветом BLACK, GREY, обоими или без указания цвета. "
                        "В ответе должен быть track.")
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        []
    ])
    def test_create_order_with_different_colors(self, color):
        """Проверяем создание заказа с разными вариантами цвета"""

        payload = OrderData.BASE_ORDER.copy()
        payload["color"] = color

        with allure.step(f"Создаём заказ с цветом: {color or 'без цвета'}"):
            response = requests.post(Urls.CREATE_ORDER, json=payload)

        with allure.step("Проверяем успешное создание заказа"):
            assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}"

        with allure.step("Проверяем, что в ответе есть track"):
            response_json = response.json()
            assert "track" in response_json, f"Поле 'track' отсутствует в ответе: {response_json}"
            assert isinstance(response_json["track"], int), "Значение track должно быть числом"
