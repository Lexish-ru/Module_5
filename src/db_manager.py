import psycopg2
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)

    def get_companies_and_vacancies_count(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT employers.name, COUNT(vacancies.id)
                FROM employers
                LEFT JOIN vacancies ON employers.id = vacancies.employer_id
                GROUP BY employers.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT title, salary, url FROM vacancies")
            return cur.fetchall()

    def get_avg_salary(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL")
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("SELECT title, salary FROM vacancies WHERE salary > %s", (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        with self.conn.cursor() as cur:
            cur.execute("SELECT title, salary, url FROM vacancies WHERE title ILIKE %s", (f"%{keyword}%",))
            return cur.fetchall()
