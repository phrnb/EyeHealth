import requests
import pytest
import time
import json

# Базовый URL NeuralNetworkService
BASE_URL = "http://localhost:8080/api/neural"


@pytest.fixture
def test_image():
    """Открывает тестовое изображение для отправки"""
    return open("test_image.jpg", "rb")


def test_neural_network_success(test_image):
    """Тест успешного предсказания нейросети"""
    files = {"file": test_image}

    start_time = time.time()  # Засекаем время выполнения
    response = requests.post(f"{BASE_URL}/predict", files=files)
    elapsed_time = time.time() - start_time

    # Проверяем код ответа
    assert response.status_code == 200, f"Ошибка: {response.status_code}, {response.text}"

    # Проверяем JSON-ответ
    json_data = response.json()
    assert "status" in json_data, "Нет ключа 'status' в ответе"
    assert json_data["status"] == "success", "Статус ответа не 'success'"

    assert "prediction" in json_data, "Нет ключа 'prediction' в ответе"
    assert "confidence" in json_data, "Нет ключа 'confidence' в ответе"

    # Проверяем диапазон уверенности (0-100%)
    confidence = json_data["confidence"]
    assert 0 <= confidence <= 100, f"Confidence {confidence} выходит за границы 0-100%"

    # Проверяем, что API отвечает быстро (< 2 сек)
    assert elapsed_time < 2, f"Ответ API слишком долгий: {elapsed_time:.2f} сек"


def test_neural_network_invalid_file():
    """Тест отправки некорректного файла (не изображение)"""
    files = {"file": ("invalid.txt", b"Not an image", "text/plain")}
    response = requests.post(f"{BASE_URL}/predict", files=files)

    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    assert "error" in response.json(), "Нет ключа 'error' в ответе"


def test_neural_network_empty_request():
    """Тест отправки пустого запроса"""
    response = requests.post(f"{BASE_URL}/predict", files={})

    assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
    assert "error" in response.json(), "Нет ключа 'error' в ответе"


def test_neural_network_server_error(monkeypatch):
    """Тест обработки ошибки сервера"""

    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 500

            def json(self):
                return {"error": "Internal Server Error"}

        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)

    response = requests.post(f"{BASE_URL}/predict", files={})
    assert response.status_code == 500, "Ожидался 500, но получен другой код"
    assert "error" in response.json(), "Нет ключа 'error' в ответе"


def test_neural_network_json_response(test_image):
    """Тест, что API всегда возвращает корректный JSON"""
    files = {"file": test_image}
    response = requests.post(f"{BASE_URL}/predict", files=files)

    try:
        json.loads(response.text)
    except json.JSONDecodeError:
        pytest.fail("Ответ API не является корректным JSON")

