import requests
from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# === Базовые настройки ===
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BASE_URL = "https://api.foursquare.com/v3/places/search"


def get_coordinates():
    """Функция получения координат"""
    return {
        "ll": "55.751244,37.618423"  # Москва
    }


def search_places(category):
    """Основная функция поиска"""
    coordinates = get_coordinates()

    headers = {
        "Authorization": ACCESS_TOKEN,
        "Accept": "application/json"
    }

    params = {
        "query": category,
        "limit": 5
    }

    params.update(coordinates)      # Добавляем координаты в параметры

    response = requests.get(BASE_URL, headers=headers, params=params)

    if response.status_code == 401:
        print("Ошибка авторизации. Проверьте ваш ACCESS_TOKEN.")
        return

    if not response.ok:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    results = data.get("results", [])

    if not results:
        print("Ничего не найдено.")
        return

    print(f"\nРезультаты по категории '{category}':\n")
    for place in results:
        name = place.get("name")
        location = place.get("location", {})
        address = location.get("formatted_address", "Адрес не указан")
        rating = place.get("rating", "Не оценен")

        print(f"Название: {name}")
        print(f"Адрес: {address}")
        print(f"Рейтинг: {rating}")
        print("-" * 40)

# === Точка входа ===
if __name__ == '__main__':
    user_category = input("Введите категорию (например, кафе, музеи, парки): ")
    search_places(user_category)