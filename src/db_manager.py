from typing import List, Optional, Tuple

import psycopg2

from src.config import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


class DBManager:
    """Класс для работы с базой данных: чтение вакансий и компаний."""

    def __init__(self) -> None:
        """Инициализирует подключение к базе данных."""
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """Возвращает список компаний с количеством их вакансий."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT employers.name, COUNT(vacancies.id)
                FROM employers
                LEFT JOIN vacancies ON employers.id = vacancies.employer_id
                GROUP BY employers.name
            """
            )
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, Optional[int], str, str]]:
        """Возвращает все вакансии с названием, зарплатой, ссылкой и работодателем."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT v.title, v.salary, v.url, e.name
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
            """
            )
            return cur.fetchall()

    def get_avg_salary(self) -> Optional[float]:
        """Возвращает среднюю зарплату по всем вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL
            """
            )
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, int, str]]:
        """Возвращает вакансии с зарплатой выше средней."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT v.title, v.salary, e.name
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE v.salary > (SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL)
            """
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, Optional[int], str]]:
        """Возвращает вакансии, в названии которых встречается ключевое слово."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT title, salary, url FROM vacancies
                WHERE title ILIKE %s
            """,
                (f"%{keyword}%",),
            )
            return cur.fetchall()

    def close(self) -> None:
        """Закрывает подключение к базе данных."""
        self.conn.close()
