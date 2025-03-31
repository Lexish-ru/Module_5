from src.db_manager import DBManager
from src.database import create_database
from src.hh_api import (
    get_top_employers,
    get_vacancies_from_hh,
    search_employer_by_name,
    add_employer_to_list
)
import psycopg2
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


def insert_data():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cur = conn.cursor()
    employers = get_top_employers()

    for employer in employers:
        # Проверка: есть ли работодатель в БД
        cur.execute("SELECT id FROM employers WHERE hh_id = %s", (employer["id"],))
        existing = cur.fetchone()

        if existing:
            employer_id = existing[0]
            print(f"Работодатель {employer['name']} уже есть в БД, id = {employer_id}")
        else:
            cur.execute(
                "INSERT INTO employers (hh_id, name) VALUES (%s, %s) RETURNING id",
                (employer["id"], employer["name"])
            )
            employer_id = cur.fetchone()[0]
            print(f"Добавлен работодатель: {employer['name']}")

        # Получаем и вставляем вакансии
        vacancies = get_vacancies_from_hh(employer["id"])
        for vacancy in vacancies:
            salary = vacancy.get("salary")
            salary_amount = salary["from"] if salary and salary.get("from") else None
            cur.execute(
                "INSERT INTO vacancies (employer_id, title, salary, url) VALUES (%s, %s, %s, %s)",
                (employer_id, vacancy["name"], salary_amount, vacancy["alternate_url"])
            )

    conn.commit()
    cur.close()
    conn.close()



def main():
    db = None  # Соединение создаём после создания базы

    while True:
        print("\n=== Меню ===")
        print("1. Создать базу данных (удалит старую!)")
        print("2. Загрузить данные с hh.ru")
        print("3. Показать компании и количество вакансий")
        print("4. Показать все вакансии")
        print("5. Показать среднюю зарплату")
        print("6. Показать вакансии с зарплатой выше средней")
        print("7. Поиск вакансий по ключевому слову")
        print("8. Добавить новую компанию в список (по названию)")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            if db:
                db.close()
            create_database()
            print("База данных создана.")
            db = DBManager()

        elif choice == "2":
            if db is None:
                db = DBManager()
            insert_data()
            print("Данные успешно загружены.")

        elif choice == "3":
            if db is None:
                db = DBManager()
            results = db.get_companies_and_vacancies_count()
            for company, count in results:
                print(f"{company}: {count} вакансий")

        elif choice == "4":
            if db is None:
                db = DBManager()
            results = db.get_all_vacancies()
            for title, salary, url, company in results:
                print(f"{title} | {salary or '—'} | {company} | {url}")

        elif choice == "5":
            if db is None:
                db = DBManager()
            avg = db.get_avg_salary()
            print(f"Средняя зарплата: {round(avg) if avg else 'Нет данных'}")

        elif choice == "6":
            if db is None:
                db = DBManager()
            results = db.get_vacancies_with_higher_salary()
            for title, salary in results:
                print(f"{title} | {salary}")

        elif choice == "7":
            if db is None:
                db = DBManager()
            keyword = input("Введите ключевое слово: ")
            results = db.get_vacancies_with_keyword(keyword)
            for title, salary, url in results:
                print(f"{title} | {salary or '—'} | {url}")

        elif choice == "8":
            name = input("Введите название компании для поиска на hh.ru: ")
            result = search_employer_by_name(name)
            if result:
                print(f"Найдена компания: {result['name']} (ID: {result['id']})")
                added = add_employer_to_list(result)
                if added:
                    print("Компания добавлена в список.")
                else:
                    print("Компания уже есть в списке.")
            else:
                print("Компания не найдена.")

        elif choice == "0":
            print("До свидания!")
            if db:
                db.close()
            break

        else:
            print("Неверный выбор. Попробуйте снова.")
