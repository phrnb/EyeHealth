import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Функция подключения к базе данных
def connect_to_db():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

# Функция для создания таблиц
def create_tables():
    conn = connect_to_db()
    cursor = conn.cursor()

    # SQL запросы для создания таблиц
    create_tables_queries = [
        """CREATE TABLE IF NOT EXISTS companies (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            role VARCHAR(50),
            password VARCHAR(255) NOT NULL,
            company INT,
            post VARCHAR(255),
            CONSTRAINT fk_users_company FOREIGN KEY (company) REFERENCES companies(id) ON DELETE SET NULL
        )""",
        """CREATE TABLE IF NOT EXISTS accounts (
            id SERIAL PRIMARY KEY,
            login VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            last_login TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""",
        """CREATE TABLE IF NOT EXISTS administrators (
            id SERIAL PRIMARY KEY,
            fio VARCHAR(255) NOT NULL,
            post VARCHAR(255),
            account_id INT UNIQUE,
            CONSTRAINT fk_admins_account FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
        )""",
        """CREATE TABLE IF NOT EXISTS patients (
            id SERIAL PRIMARY KEY,
            owner_id INT,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            gender VARCHAR(10),
            birth_date DATE,
            phone_number VARCHAR(20),
            address TEXT,
            number VARCHAR(50),
            CONSTRAINT fk_patients_owner FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
        )""",
        """CREATE TABLE IF NOT EXISTS diagnosis (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT
        )""",
        """CREATE TABLE IF NOT EXISTS photos (
            id SERIAL PRIMARY KEY,
            patient_id INT,
            data BYTEA,
            ready BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            ready_at TIMESTAMP,
            description TEXT,
            diagnosis INT,
            CONSTRAINT fk_photos_patient FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            CONSTRAINT fk_photos_diagnosis FOREIGN KEY (diagnosis) REFERENCES diagnosis(id) ON DELETE SET NULL
        )""",
        """CREATE TABLE IF NOT EXISTS analyze_queue (
            id SERIAL PRIMARY KEY,
            owner_id INT,
            patient_id INT,
            photo_id INT,
            ready BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_analyze_owner FOREIGN KEY (owner_id) REFERENCES accounts(id) ON DELETE CASCADE,
            CONSTRAINT fk_analyze_patient FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            CONSTRAINT fk_analyze_photo FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE SET NULL
        )"""
    ]

    # Выполнение всех запросов
    for query in create_tables_queries:
        cursor.execute(query)

    # Подтверждение изменений и закрытие соединения
    conn.commit()
    cursor.close()
    conn.close()

# Вызов функции для создания таблиц
create_tables()