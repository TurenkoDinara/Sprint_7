import pytest
import allure
from helpers import CourierHelpers

@pytest.fixture
def delete_courier_after_test():
    """Фикстура: удаляет курьера после теста, если он был создан"""
    created_couriers = []

    yield created_couriers  # передаём список для заполнения из теста

    for courier_data in created_couriers:
        with allure.step("Удаляем курьера после теста"):
            courier_id = CourierHelpers.get_courier_id(courier_data["login"], courier_data["password"])
            if courier_id:
                CourierHelpers.delete_courier(courier_id)

@pytest.fixture
def create_and_delete_courier():
    """Фикстура: создает курьера и удаляет его после теста"""
    with allure.step("Создать тестового курьера"):
        create_response, courier_data = CourierHelpers.create_courier()
        assert create_response.status_code == 201, f"Не удалось создать курьера. Ответ: {create_response.status_code} {create_response.text}"

    yield courier_data

    with allure.step("Удалить тестового курьера"):
        courier_id = CourierHelpers.get_courier_id(courier_data["login"], courier_data["password"])
        if courier_id:
            CourierHelpers.delete_courier(courier_id)
