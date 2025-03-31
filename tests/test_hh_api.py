
import unittest
from unittest.mock import patch, mock_open
from src.hh_api import (search_employer_by_name, get_top_employers,
                        get_vacancies_from_hh, save_employers, load_employers)
import json


MOCK_VACANCIES = {
    "items": [
        {"name": "Python Dev", "salary": {"from": 100000}, "alternate_url": "url1"},
        {"name": "Backend", "salary": None, "alternate_url": "url2"},
    ]
}


class TestHHAPI(unittest.TestCase):

    @patch("src.hh_api.requests.get")
    def test_search_employer_mocked(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "items": [{"id": "1455", "name": "Яндекс"}]
        }
        result = search_employer_by_name("Яндекс")
        self.assertEqual(result["id"], "1455")
        self.assertEqual(result["name"], "Яндекс")

    def test_get_top_employers_structure(self):
        employers = get_top_employers()
        self.assertIsInstance(employers, list)
        for emp in employers:
            self.assertIn("id", emp)
            self.assertIn("name", emp)


class TestHHAPIExtended(unittest.TestCase):

    @patch("src.hh_api.requests.get")
    def test_get_vacancies_from_hh(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = MOCK_VACANCIES
        result = get_vacancies_from_hh("123")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["name"], "Python Dev")

    @patch("builtins.open", new_callable=mock_open)
    def test_save_employers(self, mock_file):
        employers = [{"id": "1", "name": "Company"}]
        save_employers(employers)
        mock_file().write.assert_called()

    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": "1", "name": "Company"}]')
    def test_load_employers(self, mock_file):
        result = load_employers()
        self.assertEqual(result[0]["id"], "1")