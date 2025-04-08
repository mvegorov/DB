import os
import psycopg2
from faker import Faker
import random

fake = Faker()

def insert_sofia(connection, num_records):
    with connection.cursor() as cursor:
        for id in range(1, num_records + 1):
            word="the best"
            cursor.execute(
                "INSERT INTO \"Sofia\" (id, word) VALUES (%s, %s)",
                (id, word)
            )
        connection.commit()

def insert_users(connection, num_records):
    with connection.cursor() as cursor:
        for user_id in range(1, num_records + 1):
            user_name = fake.name()
            level = random.choice(['A', 'B', 'C'])
            is_verified = random.choice([True, False])
            is_editor = random.choice([True, False])
            subscribe_end = fake.time()  # Генерация времени подписки
            cursor.execute(
                "INSERT INTO \"User\" (user_id, user_name, level, is_verified, is_editor, subscribe_end) VALUES (%s, %s, %s, %s, %s, %s)",
                (user_id, user_name, level, is_verified, is_editor, subscribe_end)
            )

        connection.commit()

def insert_categories(connection, num_records):
    with connection.cursor() as cursor:
        for category_id in range(1, num_records + 1):
            category_name = fake.word()
            cursor.execute(
                "INSERT INTO \"Category\" (category_id, category_name) VALUES (%s, %s)",
                (category_id, category_name)
            )
        connection.commit()

def insert_subcategories(connection, num_records):
    """Заполняет таблицу Subcategory тестовыми данными."""
    with connection.cursor() as cursor:
        for subcategory_id in range(1, num_records + 1):
            category_id = random.randint(1, num_records)  # Случайная категория
            subcategory_name = fake.word()
            cursor.execute(
                "INSERT INTO \"Subcategory\" (subcategory_id, category_id, subcategory_name) VALUES (%s, %s, %s)",
                (subcategory_id, category_id, subcategory_name)
            )
        connection.commit()

def insert_words(connection, num_records):
    """Заполняет таблицу Word тестовыми данными."""
    with connection.cursor() as cursor:
        for word_id in range(1, num_records + 1):
            word = fake.word()
            meaning_A = fake.sentence()
            meaning_B = fake.sentence()
            meaning_C = fake.sentence()
            level = random.choice(['A', 'B', 'C'])
            subcategory_id = random.randint(1, num_records)  # Случайная подкатегория
            tags = ', '.join(fake.words(random.randint(1, 5)))  # Случайные теги
            cursor.execute(
                "INSERT INTO \"Word\" (word_id, word, meaning_A, meaning_B, meaning_C, level, subcategory_id, tags) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (word_id, word, meaning_A, meaning_B, meaning_C, level, subcategory_id, tags)
            )
        connection.commit()

def insert_collections(connection, num_records):
    """Заполняет таблицу Collection тестовыми данными."""
    with connection.cursor() as cursor:
        for collection_id in range(1, num_records + 1):
            user_id = random.randint(1, num_records)  # Случайный пользователь
            description = fake.sentence()
            cursor.execute(
                "INSERT INTO \"Collection\" (collection_id, user_id, description) VALUES (%s, %s, %s)",
                (collection_id, user_id, description)
            )
        connection.commit()

def insert_collections_info(connection, num_records):
    """Заполняет таблицу Collections_Info тестовыми данными."""
    with connection.cursor() as cursor:
        for word_id in range(1, num_records // 10 + 1):
            collection_id = random.randint(1, num_records // 10)  # Случайная коллекция
            meaning = fake.sentence()
            cursor.execute(
                "INSERT INTO \"Collections_Info\" (word_id, collection_id, meaning) VALUES (%s, %s, %s)",
                (word_id, collection_id, meaning)
            )
        connection.commit()

def insert_studying_session(connection, num_records):
    """Заполняет таблицу Studying_session тестовыми данными."""
    with connection.cursor() as cursor:
        for session_id in range(1, num_records+1):
            collection_id = random.randint(1, num_records)  # Случайная коллекция
            user_id = random.randint(1, num_records)  # Случайный пользователь
            time_start = fake.time()
            duration = fake.time()  # Генерация продолжительности
            total_words = random.randint(1, 100)  # Случайное количество слов
            cursor.execute(
                "INSERT INTO \"Studying_session\" (session_id, collection_id, user_id, time_start, duration, total_words) VALUES (%s, %s, %s, %s, %s, %s)",
                (session_id, collection_id, user_id, time_start, duration, total_words)
            )
        connection.commit()

def insert_users_progress(connection, num_records):
    """Заполняет таблицу Users_progress тестовыми данными."""
    with connection.cursor() as cursor:
        for user_id in range(1, num_records+1):
            word_id = random.randint(1, num_records)  # Случайное слово
            last_success = fake.time()
            successes_in_row = random.randint(1, 10)  # Случайное количество успехов подряд
            cursor.execute(
                "INSERT INTO \"Users_progress\" (user_id, word_id, last_success, successes_in_row) VALUES (%s, %s, %s, %s)",
                (user_id, word_id, last_success, successes_in_row)
            )
        connection.commit()

def insert_editing_log(connection, num_records):
    """Заполняет таблицу Editing_log тестовыми данными."""
    with connection.cursor() as cursor:
        for log_id in range(1, num_records + 1):
            user_id = random.randint(1, num_records)  # Случайный пользователь
            word_id = random.randint(1, num_records)  # Случайное слово
            log_text = fake.sentence()
            cursor.execute(
                "INSERT INTO \"Editing_log\" (log_id, user_id, word_id, log_text) VALUES (%s, %s, %s, %s)",
                (log_id, user_id, word_id, log_text)
            )
        connection.commit()

def truncate_tables(connection):
    """Очищает все таблицы в базе данных."""
    with connection.cursor() as cursor:
        # Список таблиц для очистки
        tables = [
            "User",
            "Category",
            "Subcategory",
            "Word",
            "Collection",
            "Collections_Info",
            "Studying_session",
            "Users_progress",
            "Editing_log"
        ]

        for table in tables:
            cursor.execute(f"TRUNCATE TABLE \"{table}\" CASCADE;")

        connection.commit()

def generate(connection, num_records):
    version = os.getenv('MIGRATION_VERSION')
    if version == '1.0.1' or version == '1.1.0':
        print("Generation started.")
        insert_users(connection, num_records)
        insert_categories(connection, num_records // 10)
        insert_subcategories(connection, num_records // 10)
        insert_words(connection, num_records // 10)
        insert_collections(connection, num_records // 10)
        insert_collections_info(connection, num_records)
        insert_studying_session(connection, num_records // 10)
        insert_users_progress(connection, num_records // 10)
        insert_editing_log(connection, num_records // 10)
        print("Data generated according to version 1.0.1 ")

    if version == '2.0.1':
        insert_sofia(connection, num_records // 10)
        print("Data generated according to version 2.0.1 ")

def main():
    if os.getenv('RUN_DATA_POPULATOR') != 'true':
        return

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    truncate_tables(connection)

    num_records=int(os.getenv('DATA_POPULATOR_NUM_RECORDS'))

    generate(connection, num_records)

    connection.close()

if __name__ == "__main__":
    main()