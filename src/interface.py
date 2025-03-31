def main():
    db = DBManager()

    while True:
        print("\n=== Меню ===")
        print("1. Создать базу данных (удалит старую!)")
        print("2. Загрузить данные с hh.ru")
        print("3. Показать компании и количество вакансий")
        print("4. Показать все вакансии")
        print("5. Показать среднюю зарплату")
        print("6. Показать вакансии с зарплатой выше средней")
        print("7. Поиск вакансий по ключевому слову")
        print("0. Выход")

        choice = input("Выберите действие: ")

        if choice == "1":
            create_database()
            print("База данных создана.")
        elif choice == "2":
            insert_data()
            print("Данные загружены.")
        elif choice == "3":
            results = db.get_companies_and_vacancies_count()
            for company, count in results:
                print(f"{company}: {count} вакансий")
        elif choice == "4":
            results = db.get_all_vacancies()
            for title, salary, url, company in results:
                print(f"{title} | {salary or '—'} | {company} | {url}")
        elif choice == "5":
            avg = db.get_avg_salary()
            print(f"Средняя зарплата: {round(avg) if avg else 'Нет данных'}")
        elif choice == "6":
            results = db.get_vacancies_with_higher_salary()
            for title, salary in results:
                print(f"{title} | {salary}")
        elif choice == "7":
            keyword = input("Введите ключевое слово: ")
            results = db.get_vacancies_with_keyword(keyword)
            for title, salary, url in results:
                print(f"{title} | {salary or '—'} | {url}")
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")
