
import unittest
from unittest.mock import patch
from src.db_manager import DBManager
from src.database import create_database
from src.interface import insert_data
import psycopg2
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

MOCK_EMPLOYERS = [{"id": "1455", "name": "Яндекс"}]
MOCK_VACANCIES = [
    {"name": "Python Developer", "salary": {"from": 150000}, "alternate_url": "https://hh.ru/vacancy/123"},
    {"name": "Backend Developer", "salary": {"from": 120000}, "alternate_url": "https://hh.ru/vacancy/456"}
]

class TestDeduplication(unittest.TestCase):

    @patch("src.interface.get_vacancies_from_hh", return_value=MOCK_VACANCIES)
    @patch("src.interface.get_top_employers", return_value=MOCK_EMPLOYERS)
    def test_employers_not_duplicated(self, mock_employers, mock_vacancies):
        create_database()
        insert_data()
        insert_data()

        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM employers")
        employer_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM vacancies")
        vacancy_count = cur.fetchone()[0]

        self.assertEqual(employer_count, 1)
        self.assertEqual(vacancy_count, 4)

        cur.close()
        conn.close()
