import pymysql
from prettytable import PrettyTable

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """Устанавливает соединение с базой данных."""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Подключение к MySQL успешно")
        except pymysql.MySQLError as e:
            print(f"Ошибка '{e}' при подключении к MySQL")

    def execute_query(self, query, params=None):
        """Выполняет SQL-запрос."""
        if self.connection is None:
            print("Соединение не установлено. Пожалуйста, подключитесь к базе данных.")
            return None

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                self.connection.commit()
                return cursor.fetchall(), cursor.description  # Возвращаем результаты и метаданные

        except pymysql.MySQLError as e:
            print(f"Ошибка '{e}' при выполнении запроса: {query}")
            return None, None  # Возвращаем None для результатов и метаданных

    def select(self, table, columns='*', where_condition=None):
        """Выбирает данные из таблицы."""
        query = f"SELECT {columns} FROM {table}"
        params = None
        if where_condition:
            where_str = ' AND '.join([f"{col} = %s" for col in where_condition.keys()])
            query += f" WHERE {where_str}"
            params = list(where_condition.values())
        return self.execute_query(query, params)

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()
            print("Соединение с MySQL закрыто")

# Пример использования
db = Database("127.0.0.1", "root", "1111", "cat_cafe")
db.connect()

# Получаем данные из таблицы "player"
result, description = db.select("player")
if result is not None and description is not None:
    # Создаем таблицу для вывода
    table = PrettyTable()
    table.field_names = [desc[0] for desc in description]  # Получаем названия колонок

    for row in result:
        table.add_row(row)

    print(table)
else:
    print("Не удалось получить данные из таблицы.")

db.close()