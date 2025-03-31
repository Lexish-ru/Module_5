
import unittest
from unittest.mock import patch
from src.interface import insert_data
from src.database import create_database

MOCK_EMPLOYERS = [{"id": "1455", "name": "Яндекс"}]
MOCK_VACANCIES = [
    {"name": "Python Developer", "salary": {"from": 150000}, "alternate_url": "https://hh.ru/vacancy/123"},
    {"name": "Backend Developer", "salary": {"from": 120000}, "alternate_url": "https://hh.ru/vacancy/456"}
]

class TestInterface(unittest.TestCase):

    @patch("src.interface.get_vacancies_from_hh", return_value=MOCK_VACANCIES)
    @patch("src.interface.get_top_employers", return_value=MOCK_EMPLOYERS)
    def test_insert_data_runs_without_error(self, mock_employers, mock_vacancies):
        create_database()
        try:
            insert_data()
        except Exception as e:
            self.fail(f"insert_data() вызвал исключение: {e}")
