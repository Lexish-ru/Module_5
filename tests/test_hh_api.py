import os
import unittest

from src.hh_api import (get_top_employers, get_vacancies_from_hh, load_employers, save_employers,
                        search_employer_by_name)


class TestHHApi(unittest.TestCase):
    """Тесты для модуля hh_api."""

    def test_search_employer_mocked(self) -> None:
        """Проверяет поиск работодателя по имени."""
        employers = [{"id": "1", "name": "Яндекс"}, {"id": "2", "name": "VK"}]
        result = search_employer_by_name("янд", employers)
        self.assertEqual(len(result), 1)

    def test_get_top_employers_structure(self) -> None:
        """Проверяет, что топ работодатели — список словарей с ключами 'id' и 'name'."""
        result = get_top_employers()
        self.assertTrue(all("id" in emp and "name" in emp for emp in result))

    def test_get_vacancies_from_hh(self) -> None:
        """Проверяет, что функция возвращает список вакансий (даже если пустой)."""
        result = get_vacancies_from_hh("nonexistent_id")
        self.assertIsInstance(result, list)

    def test_save_employers(self) -> None:
        """Проверяет, что функция сохраняет работодателей в файл."""
        test_data = [{"id": "3", "name": "Тест"}]
        save_employers(test_data)
        self.assertTrue(os.path.exists("employers.json"))

    def test_load_employers(self) -> None:
        """Проверяет, что данные успешно загружаются из файла."""
        data = load_employers()
        self.assertIsInstance(data, list)
