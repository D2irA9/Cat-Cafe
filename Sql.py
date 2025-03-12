import pymysql
from prettytable import PrettyTable
import hashlib
from datetime import datetime

class Database:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "root"
        self.password = "1111"
        self.database = "cat_cafe"
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
                return cursor.fetchall(), cursor.description

        except pymysql.MySQLError as e:
            print(f"Ошибка '{e}' при выполнении запроса: {query}")
            return None, None

    def encrypt_password(self, password):
        """Шифрует пароль с использованием MD5."""
        return hashlib.md5(password.encode()).hexdigest()

    def add_player(self, name, email, password, balance=100, day=1):
        """Добавление игрока"""
        
        # Шифрование пароля
        encrypted_password = self.encrypt_password(password)

        query = "INSERT INTO `player` (name, day, balance, email, password, regist_date) VALUES (%s, %s, %s, %s, %s, NOW())"
        params = (name, day, balance, email, encrypted_password)

        result, _ = self.execute_query(query, params)
        if result is not None:
            print("Игрок успешно добавлен.")
        else:
            print("Не удалось добавить игрока.")

    def close(self):
        """Закрывает соединение с базой данных."""
        if self.connection:
            self.connection.close()
            print("Соединение с MySQL закрыто")