import pymysql
import bcrypt

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
                return cursor.fetchall()  # Возвращаем все результаты запроса

        except pymysql.MySQLError as e:
            print(f"Ошибка '{e}' при выполнении запроса: {query}")
            return None

    def add_MenuClient(self):
        """Добавления записи"""
        query_menu = "INSERT INTO `menu` (id, name, price) VALUES (%s, %s, %s);"
        menu_items = [
            (1, "Pasta", 51),
            (2, "Tacos", 17),
            (3, "Ramen", 33),
            (4, "Hamburg", 29),
            (5, "Pizza", 41),
            (6, "Rolls", 31),
            (7, "Soup", 19),
            (8, "Fried_egg", 11),
            (9, "Water", 5),
            (10, "Cocoa", 16),
            (11, "Tea", 12),
            (12, "Milkshake", 20),
            (13, "Coffee", 17),
            (14, "Cocktail", 18),
            (15, "Lemonade", 15),
            (16, "Soda", 15),
            (17, "Cupcake", 19),
            (18, "Cheesecake", 23),
            (19, "Cake", 25),
            (20, "Ice_cream", 25),
            (21, "Pie", 30)
        ]
        query_client = "INSERT INTO `client` (id, name, preferences) VALUES (%s, %s, %s);"
        client_items = [
            (1, "Lyubava", 12),
            (2, "Panteleimon", 3),
            (3, "Vasiliy", 19),
            (4, "Khariton", 7),
            (5, "Nona", 20),
            (6, "Yevsey", 17),
            (7, "Kostya", 21),
            (8, "Viola", 6)
        ]
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(query_menu, menu_items)
                print(f"{cursor.rowcount} записей успешно добавлено в меню.")

                cursor.executemany(query_client, client_items)
                print(f"{cursor.rowcount} записей успешно добавлено в клиентов.")

                self.connection.commit()
        except pymysql.MySQLError as e:
            print(f"Ошибка '{e}' при добавлении записей.")


    def creating_tables(self):
        """Создание таблиц"""
        create_player_table_quey = """CREATE TABLE IF NOT EXISTS `player`( 
            `id` INT NOT NULL AUTO_INCREMENT,            
            `name` VARCHAR(100) NOT NULL,
            `day` INT NOT NULL,
            `balance` INT NOT NULL,
            `email` VARCHAR(255) NOT NULL,
            `password` VARCHAR(255) NOT NULL,
            `regist_date` DATE NOT NULL,
            PRIMARY KEY (`id`) USING BTREE
        );"""
        create_menu_table_quey = """CREATE TABLE IF NOT EXISTS `menu` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(100) NOT NULL,
            `price` INT NOT NULL,
            PRIMARY KEY (`id`) USING BTREE
            );"""
        create_client_table_quey = """CREATE TABLE IF NOT EXISTS `client` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `name` VARCHAR(100) NOT NULL,
            `preferences` INT NOT NULL,
            PRIMARY KEY (`id`) USING BTREE,
            INDEX `preferences` (`preferences`) USING BTREE,
            CONSTRAINT `preferences` FOREIGN KEY (`preferences`) REFERENCES `menu` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
        );"""
        create_orders_table_quey = """CREATE TABLE IF NOT EXISTS `orders` (
            `id` INT NOT NULL,
            `player_id` INT NOT NULL,
            `client_id` INT NOT NULL,
            `dish_id` INT NOT NULL,
            PRIMARY KEY (`id`) USING BTREE,
            INDEX `player_id` (`player_id`) USING BTREE,
            INDEX `client_id` (`client_id`) USING BTREE,
            INDEX `dish_id` (`dish_id`) USING BTREE,
            CONSTRAINT `client_id` FOREIGN KEY (`client_id`) REFERENCES `client` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
            CONSTRAINT `dish_id` FOREIGN KEY (`dish_id`) REFERENCES `menu` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
            CONSTRAINT `player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`) ON UPDATE NO ACTION ON DELETE NO ACTION
        );"""
        self.execute_query(create_player_table_quey)
        self.execute_query(create_menu_table_quey)
        self.execute_query(create_client_table_quey)
        self.execute_query(create_orders_table_quey)
        print("Таблицы созданы или уже существуют")
        self.add_MenuClient()

    def encrypt_password(self, password):
        """Шифрует пароль"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_player_exists(self, player_id):
        """Проверяет, существует ли игрок с данным ID"""
        query = "SELECT player.id FROM `player` WHERE `id` = %s"
        result = self.execute_query(query, (player_id,))
        return result is not None and len(result) > 0

    def add_player(self, name, email, password, balance=100, day=1):
        """Добавление игрока"""

        # Шифрование пароля
        encrypted_password = self.encrypt_password(password)

        query = "INSERT INTO `player` (name, day, balance, email, password, regist_date) VALUES (%s, %s, %s, %s, %s, NOW())"
        params = (name, day, balance, email, encrypted_password)

        self.execute_query(query, params)
        print("Игрок успешно добавлен.")

    def check_user(self, email, password):
        """Проверяет, существует ли пользователь с данным email и паролем."""
        query = "SELECT password FROM player WHERE email = %s"
        result = self.execute_query(query, (email,))

        if result and len(result) > 0:
            stored_password = result[0][0]
            return bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8'))
        return False

    def get_player_id(self, email):
        """Получает ID игрока по email"""
        query = "SELECT id FROM player WHERE email = %s"
        result = self.execute_query(query, (email,))

        if result and len(result) > 0:
            return result[0][0]  # Возвращаем ID игрока
        return None  # Если игрок не найден, возвращаем None

    def get_player_balance(self, player_id):
        """Получает баланс игрока по ID"""
        query = "SELECT balance FROM player WHERE id = %s"
        result, _ = self.execute_query(query, (player_id,))
        return result[0][0] if result else None

    def update_balance(self, player_id, new_balance):
        """Обновляет баланс игрока в базе данных"""
        if not self.check_player_exists(player_id):
            print(f"Игрок с ID {player_id} не найден.")
            return

        query = "UPDATE player SET balance = %s WHERE id = %s"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, (new_balance, player_id))
                self.connection.commit()
                print(f"Баланс игрока с ID {player_id} обновлен на {new_balance}.")
        except Exception as e:
            print(f"Ошибка при обновлении баланса: {e}")

    def get_menu_items(self):
        """Получает список всех блюд и их цен из базы данных."""
        query = "SELECT name, price FROM menu"
        result = self.execute_query(query)
        if result:
            return {item[0]: item[1] for item in result}
        return None

    def close(self):
        """Закрывает соединение с базой данных"""
        if self.connection:
            self.connection.close()
            print("Соединение с MySQL закрыто")