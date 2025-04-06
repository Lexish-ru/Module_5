import unittest
from unittest.mock import MagicMock, patch

from src.interface import (get_user_input, insert_data, search_vacancies_by_keyword, show_all_vacancies,
                           show_avg_salary, show_companies_and_vacancies, show_high_salary_vacancies)


class TestInterface(unittest.TestCase):
    """Тесты для пользовательского интерфейса и обёрток над DBManager."""

    @patch("src.hh_api.save_employers")
    @patch(
        "src.interface.get_vacancies_from_hh",
        return_value=[{"name": "Python Dev", "salary": {"from": 100000}, "alternate_url": "https://hh.ru/vacancy/1"}],
    )
    @patch("src.interface.get_top_employers", return_value=[{"id": "123", "name": "TestCompany"}])
    @patch("src.interface.create_database")
    @patch("src.interface.DBManager")
    def test_insert_data_runs_without_error(
        self: unittest.TestCase,
        mock_db: MagicMock,
        mock_create_db: MagicMock,
        mock_top_emp: MagicMock,
        mock_get_vacs: MagicMock,
        mock_save: MagicMock,
    ) -> None:
        """Проверяет, что функция insert_data не вызывает исключений."""
        try:
            insert_data()
        except Exception as e:
            self.fail(f"insert_data вызвала исключение: {e}")

    @patch("builtins.input", return_value="list")
    def test_get_user_input(self: unittest.TestCase, mock_input: MagicMock) -> None:
        """Проверяет, что get_user_input возвращает строку."""
        result: str = get_user_input("Введите что-нибудь: ")
        self.assertIsInstance(result, str)

    @patch("builtins.print")
    @patch("src.interface.DBManager")
    def test_show_companies_and_vacancies(self: unittest.TestCase, mock_db: MagicMock, mock_print: MagicMock) -> None:
        """Проверяет вызов вывода компаний и их вакансий."""
        mock_db.return_value.get_companies_and_vacancies_count.return_value = [("Компания", 5)]
        show_companies_and_vacancies()
        self.assertTrue(mock_print.called)

    @patch("builtins.print")
    @patch("src.interface.DBManager")
    def test_show_all_vacancies(self: unittest.TestCase, mock_db: MagicMock, mock_print: MagicMock) -> None:
        """Проверяет вывод всех вакансий."""
        mock_db.return_value.get_all_vacancies.return_value = [("Разработчик", 150000, "https://url", "Компания")]
        show_all_vacancies()
        self.assertTrue(mock_print.called)

    @patch("builtins.print")
    @patch("src.interface.DBManager")
    def test_show_avg_salary(self: unittest.TestCase, mock_db: MagicMock, mock_print: MagicMock) -> None:
        """Проверяет вывод средней зарплаты."""
        mock_db.return_value.get_avg_salary.return_value = 130000
        show_avg_salary()
        self.assertTrue(mock_print.called)

    @patch("builtins.print")
    @patch("src.interface.DBManager")
    def test_show_high_salary_vacancies(self: unittest.TestCase, mock_db: MagicMock, mock_print: MagicMock) -> None:
        """Проверяет вывод вакансий с высокой ЗП."""
        mock_db.return_value.get_vacancies_with_higher_salary.return_value = [("Dev", 160000, "Компания")]
        show_high_salary_vacancies()
        self.assertTrue(mock_print.called)

    @patch("builtins.input", return_value="Python")
    @patch("builtins.print")
    @patch("src.interface.DBManager")
    def test_search_vacancies_by_keyword(
        self: unittest.TestCase, mock_db: MagicMock, mock_print: MagicMock, mock_input: MagicMock
    ) -> None:
        """Проверяет поиск вакансий по ключевому слову."""
        mock_db.return_value.get_vacancies_with_keyword.return_value = [("Python Dev", 120000, "https://url")]
        search_vacancies_by_keyword()
        self.assertTrue(mock_print.called)
