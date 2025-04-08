import os

import psycopg2

ANALYTIC_USER = os.getenv("ANALYTIC_NAME")
ANALYTIC_USER_PASSWORD = os.getenv("ANALYTIC_PASSWORD")
TABLE_NAME = os.getenv("TABLE_NAME")

num_of_users=int(os.getenv('NUM_OF_USERS'))

USERS = [["user"+str(i), "password"+str(i)] for i in range(2, num_of_users+2)]

# Функция для выполнения SQL-команды
def execute_sql(connection, query):
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()
    except psycopg2.errors.DuplicateObject:
        print(f"Exception in query \"{query}\": Already exists.")
        connection.rollback()

# Основная функция
def main():
    # Устанавливаем соединение с базой данных
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD")
    )

    try:
        # Создание ролей
        execute_sql(connection, "CREATE ROLE reader NOINHERIT;")
        execute_sql(connection, "CREATE ROLE writer NOINHERIT;")
        execute_sql(connection, "CREATE ROLE group_role NOLOGIN;")

        # Даем права ролям
        execute_sql(connection, "GRANT SELECT ON ALL TABLES IN SCHEMA public TO reader;")
        execute_sql(connection, "GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO writer;")
        execute_sql(connection, "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO group_role;")

        # Создание пользователя analytic и даем ему доступ на чтение одной таблицы
        execute_sql(connection, f"CREATE USER {ANALYTIC_USER} WITH PASSWORD '{ANALYTIC_USER_PASSWORD}';")
        execute_sql(connection, f"GRANT reader TO {ANALYTIC_USER};")
        execute_sql(connection, f"GRANT SELECT ON \"{TABLE_NAME}\" TO {ANALYTIC_USER};")

        # Создание пользователей с присоединением к групповой роли
        for user in USERS:
            execute_sql(connection, f"CREATE USER {user[0]} WITH PASSWORD '{user[1]}';")
            execute_sql(connection, f"GRANT group_role TO {user[0]};")

        print("Success.")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        connection.close()

if __name__ == "__main__":
    main()