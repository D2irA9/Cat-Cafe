import json
import os

current_player_id = None
current_player_email = None
current_player_balance = None
current_player_name = None
SAVE_FILE = "player_data.json"
first_login = True

def save_player_data():
    """Сохраняет данные игрока в файл"""
    data = {
        "id": current_player_id,
        "email": current_player_email,
        "balance": current_player_balance,
        "name": current_player_name,
        "first_login": first_login
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(data, f)


def load_player_data():
    """Загружает данные игрока из файла"""
    global current_player_id, current_player_email, current_player_balance, current_player_name, first_login

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                current_player_id = data.get("id")
                current_player_email = data.get("email")
                current_player_balance = data.get("balance")
                current_player_name = data.get("name")
                first_login = data.get("first_login", True)  # По умолчанию True, если нет в файле
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            clear_player_data()

def clear_player_data():
    """Очищает сохраненные данные"""
    global current_player_id, current_player_email, current_player_balance, current_player_name
    current_player_id = None
    current_player_email = None
    current_player_balance = None
    current_player_name = None
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


# При импорте сразу загружаем сохраненные данные
load_player_data()