import psycopg2

# Подключение к базе данных (не к той, которую мы хотим создать)
connection = psycopg2.connect(
    user="postgres",
    password="12345678",
    host="localhost",
    port="5432",
    dbname="MyEnglishVocabulary"  # Подключаемся к стандартной базе данных
)

# Создание курсора
cursor = connection.cursor()

# Выполнение команды создания базы данных
cursor.execute('SELECT * FROM public.new_table;')

# Закрытие курсора и соединения
cursor.close()
connection.commit()  # Зафиксируйте изменения
connection.close()
