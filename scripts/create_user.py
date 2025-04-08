import os
import psycopg2

# Получаем данные из переменных окружения
db_host = os.getenv('DB_HOST', 'db')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_name = os.getenv('POSTGRES_DB')
db_creator_user = os.getenv('DB_CREATOR_USER')
db_creator_password = os.getenv('DB_CREATOR_PASSWORD')

# Подключаемся к базе данных
connection = psycopg2.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    dbname=db_name
)

connection.autocommit = True
cursor = connection.cursor()

# Проверяем и создаем пользователя, если его нет
try:
    cursor.execute(f"""
    DO $$ 
    BEGIN 
        IF NOT EXISTS (
            SELECT FROM pg_catalog.pg_roles WHERE rolname = '{db_creator_user}'
        ) THEN 
            CREATE ROLE {db_creator_user} LOGIN PASSWORD '{db_creator_password}';
            GRANT ALL PRIVILEGES ON SCHEMA public TO {db_creator_user};
        END IF; 
    END $$;
    """)
    print(f"User {db_creator_user} has been created or already exists.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cursor.close()
    connection.close()
