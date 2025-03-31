
import unittest
from unittest.mock import patch
from src.interface import (
    show_companies_and_vacancies,
    show_all_vacancies,
    show_avg_salary,
    show_high_salary_vacancies,
    search_vacancies_by_keyword, get_user_input, insert_data
)
from src.database import create_database, reset_tables

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
        reset_tables()
        try:
            insert_data()
        except Exception as e:
            self.fail(f"insert_data() вызвал исключение: {e}")

class TestInterfaceInput(unittest.TestCase):

    @patch("builtins.input", return_value="python")
    def test_get_user_input(self, mock_input):
        result = get_user_input("Введите ключевое слово: ")
        self.assertEqual(result, "python")


class TestInterfaceInput(unittest.TestCase):

    @patch("builtins.input", return_value="python")
    def test_get_user_input(self, mock_input):
        result = get_user_input("Введите ключевое слово: ")
        self.assertEqual(result, "python")


class TestInterfaceShow(unittest.TestCase):

    @patch("src.interface.DBManager")
    def test_show_companies_and_vacancies(self, mock_db):
        instance = mock_db.return_value
        instance.get_companies_and_vacancies_count.return_value = [
            ("Yandex", 10),
            ("VK", 5),
        ]
        show_companies_and_vacancies()
        instance.get_companies_and_vacancies_count.assert_called_once()

    @patch("src.interface.DBManager")
    def test_show_all_vacancies(self, mock_db):
        instance = mock_db.return_value
        instance.get_all_vacancies.return_value = [
            ("Yandex", "Python Dev", 150000, "url1")
        ]
        show_all_vacancies()
        instance.get_all_vacancies.assert_called_once()

    @patch("src.interface.DBManager")
    def test_show_avg_salary(self, mock_db):
        instance = mock_db.return_value
        instance.get_avg_salary.return_value = 123456
        show_avg_salary()
        instance.get_avg_salary.assert_called_once()

    @patch("src.interface.DBManager")
    def test_show_high_salary_vacancies(self, mock_db):
        instance = mock_db.return_value
        instance.get_vacancies_with_higher_salary.return_value = [
            ("Senior Dev", 200000, "VK")
        ]
        show_high_salary_vacancies()
        instance.get_vacancies_with_higher_salary.assert_called_once()

    @patch("src.interface.get_user_input", return_value="python")
    @patch("src.interface.DBManager")
    def test_search_vacancies_by_keyword(self, mock_db, mock_input):
        instance = mock_db.return_value
        instance.get_vacancies_with_keyword.return_value = [
            ("Python Dev", 170000, "url3")
        ]
        search_vacancies_by_keyword()
        instance.get_vacancies_with_keyword.assert_called_once_with("python")