
import unittest
from src.db_manager import DBManager
from src.database import create_database, reset_tables
from unittest.mock import patch

MOCK_EMPLOYERS = [{"id": "1455", "name": "Яндекс"}]
MOCK_VACANCIES = [
    {"name": "Python Developer", "salary": {"from": 150000}, "alternate_url": "https://hh.ru/vacancy/123"},
    {"name": "Backend Developer", "salary": {"from": 120000}, "alternate_url": "https://hh.ru/vacancy/456"}
]

class TestDBManager(unittest.TestCase):

    @classmethod
    @patch("src.interface.get_vacancies_from_hh", return_value=MOCK_VACANCIES)
    @patch("src.interface.get_top_employers", return_value=MOCK_EMPLOYERS)
    def setUpClass(cls, mock_employers, mock_vacancies):
        from src.interface import insert_data
        create_database()
        reset_tables()
        insert_data()
        cls.db = DBManager()

    @classmethod
    def tearDownClass(cls):
        cls.db.close()

    def test_companies_count(self):
        companies = self.db.get_companies_and_vacancies_count()
        self.assertIsInstance(companies, list)
        self.assertGreaterEqual(len(companies), 1)

    def test_all_vacancies(self):
        vacancies = self.db.get_all_vacancies()
        self.assertIsInstance(vacancies, list)
        self.assertEqual(len(vacancies[0]), 4)

    def test_avg_salary(self):
        avg = self.db.get_avg_salary()
        self.assertTrue(avg is None or isinstance(avg, (int, float)))

    def test_higher_salary(self):
        vacancies = self.db.get_vacancies_with_higher_salary()
        self.assertIsInstance(vacancies, list)

    def test_keyword_search(self):
        results = self.db.get_vacancies_with_keyword("Python")
        self.assertIsInstance(results, list)
