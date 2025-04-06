import unittest
from decimal import Decimal
from unittest.mock import patch

from src.database import create_database, reset_tables
from src.db_manager import DBManager

MOCK_EMPLOYERS = [{"id": "1455", "name": "Яндекс"}]
MOCK_VACANCIES = [
    {"name": "Python Developer", "salary": {"from": 150000}, "alternate_url": "https://hh.ru/vacancy/123"},
    {"name": "Backend Developer", "salary": {"from": 120000}, "alternate_url": "https://hh.ru/vacancy/456"},
]


class TestDBManager(unittest.TestCase):
    """Тесты для класса DBManager."""

    @classmethod
    @patch("src.interface.get_vacancies_from_hh", return_value=MOCK_VACANCIES)
    @patch("src.interface.get_top_employers", return_value=MOCK_EMPLOYERS)
    def setUpClass(cls, mock_employers, mock_vacancies) -> None:
        """Создаёт тестовую БД и наполняет её данными."""
        from src.interface import insert_data

        create_database()
        reset_tables()
        insert_data()
        cls.db = DBManager()

    @classmethod
    def tearDownClass(cls) -> None:
        """Закрывает соединение с БД после всех тестов."""
        cls.db.close()

    def test_companies_count(self) -> None:
        """Тестирует получение количества вакансий у компаний."""
        companies = self.db.get_companies_and_vacancies_count()
        self.assertIsInstance(companies, list)
        self.assertGreaterEqual(len(companies), 1)

    def test_all_vacancies(self) -> None:
        """Тестирует получение всех вакансий с деталями."""
        vacancies = self.db.get_all_vacancies()
        self.assertIsInstance(vacancies, list)
        self.assertEqual(len(vacancies[0]), 4)

    def test_avg_salary(self) -> None:
        """Тестирует вычисление средней зарплаты."""
        avg = self.db.get_avg_salary()
        self.assertIsInstance(avg, (int, float, Decimal, type(None)))

    def test_higher_salary(self) -> None:
        """Тестирует фильтрацию вакансий с ЗП выше средней."""
        vacancies = self.db.get_vacancies_with_higher_salary()
        self.assertIsInstance(vacancies, list)

    def test_keyword_search(self) -> None:
        """Тестирует поиск вакансий по ключевому слову."""
        results = self.db.get_vacancies_with_keyword("Python")
        self.assertIsInstance(results, list)
