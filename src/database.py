import psycopg2
from src.config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST

def create_database():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employers (
            id SERIAL PRIMARY KEY,
            hh_id INT UNIQUE NOT NULL,
            name TEXT NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(id),
            title TEXT NOT NULL,
            salary INTEGER,
            url TEXT
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def reset_tables():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
    cur = conn.cursor()
    cur.execute("DELETE FROM vacancies")
    cur.execute("DELETE FROM employers")
    conn.commit()
    cur.close()
    conn.close()
