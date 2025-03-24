import requests
from src.config import API_URL

def get_vacancies_from_hh(employer_id):
    params = {"employer_id": employer_id, "per_page": 100}
    response = requests.get(API_URL, params=params)
    return response.json()["items"] if response.status_code == 200 else []

def get_top_employers():
    return [
        {"id": "1455", "name": "Яндекс"},
        {"id": "78638", "name": "Сбер"},
        {"id": "1740", "name": "VK"}
    ]
