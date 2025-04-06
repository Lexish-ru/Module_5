import json
from typing import Any, Dict, List

import requests

from src.config import API_URL


def get_vacancies_from_hh(employer_id: str) -> List[Dict[str, Any]]:
    """Получает список вакансий от HH API для заданного работодателя."""
    params = {"employer_id": employer_id, "per_page": 100}
    response = requests.get(API_URL, params=params)
    return response.json().get("items", []) if response.status_code == 200 else []


def load_employers() -> List[Dict[str, str]]:
    """Загружает список работодателей из локального JSON-файла."""
    with open("employers.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_employers(employers: List[Dict[str, str]]) -> None:
    """Сохраняет список работодателей в локальный JSON-файл."""
    with open("employers.json", "w", encoding="utf-8") as f:
        json.dump(employers, f, ensure_ascii=False, indent=2)


def get_top_employers() -> List[Dict[str, str]]:
    """Возвращает список работодателей по умолчанию (ТОП-3)."""
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
        {"id": "127955", "name": "Уралвагонзавод"},
    ]


def search_employer_by_name(name: str, employers: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Ищет работодателей по части имени (без учёта регистра)."""
    return [e for e in employers if name.lower() in e["name"].lower()]


def add_employer_to_list(employer: Dict[str, str], employers: List[Dict[str, str]]) -> None:
    """Добавляет работодателя в список, если его там ещё нет."""
    if employer not in employers:
        employers.append(employer)
