
import unittest
from unittest.mock import patch
from src.hh_api import search_employer_by_name, get_top_employers

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
