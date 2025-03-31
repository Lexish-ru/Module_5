import requests
import json
import os
from src.config import API_URL

EMPLOYERS_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
EMPLOYERS_FILE = os.path.join(EMPLOYERS_DIR, "employers.json")


def get_vacancies_from_hh(employer_id):
    params = {"employer_id": employer_id, "per_page": 100}
    response = requests.get(API_URL, params=params)
    return response.json()["items"] if response.status_code == 200 else []


def load_employers():
    if not os.path.exists(EMPLOYERS_FILE):
        return [
            {"id": "1455", "name": "Яндекс"},
            {"id": "1740", "name": "VK"},
            {"id": "3529", "name": "Тинькофф"},
            {"id": "78638", "name": "Сбер"},
            {"id": "4181", "name": "Газпром нефть"},
            {"id": "15478", "name": "ЛУКОЙЛ"},
            {"id": "4497", "name": "Роснефть"},
            {"id": "4934", "name": "КАМАЗ"},
            {"id": "3127", "name": "FESCO"},
            {"id": "127955", "name": "Уралвагонзавод"}
        ]
    with open(EMPLOYERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_employers(employers):
    os.makedirs(EMPLOYERS_DIR, exist_ok=True)
    with open(EMPLOYERS_FILE, "w", encoding="utf-8") as f:
        json.dump(employers, f, indent=2, ensure_ascii=False)


def get_top_employers():
    return load_employers()


def search_employer_by_name(name):
    url = "https://api.hh.ru/employers"
    params = {"text": name, "area": 113}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        items = response.json().get("items", [])
        if not items:
            return None
        top = items[0]
        return {"id": top["id"], "name": top["name"]}
    return None


def add_employer_to_list(employer):
    employers = load_employers()
    if any(e["id"] == employer["id"] for e in employers):
        return False
    employers.append(employer)
    save_employers(employers)
    return True
