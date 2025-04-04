import json
import os

# Глобальные переменные для хранения данных игрока
current_player_id = None
current_player_email = None
current_player_balance = None
current_player_name = None
SAVE_FILE = "player_data.json"

def save_player_data(id, email, balance, name):
    current_player_id = id
    current_player_email = email
    current_player_balance = balance
    current_player_name = name
    """Сохраняет данные игрока в файл"""
    data = {
        "id": current_player_id,
        "email": current_player_email,
        "balance": current_player_balance,
        "name": current_player_name
    }
    print(f"Сохраняем данные: {data}")
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_player_data():
    """Загружает данные игрока из файла"""
    global current_player_id, current_player_email, current_player_balance, current_player_name

    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                current_player_id = data.get("id")
                current_player_email = data.get("email")
                current_player_balance = data.get("balance")
                current_player_name = data.get("name")
                print(f"Загруженные данные: {data}")
        except json.JSONDecodeError:
            print("Ошибка: файл поврежден. Очищаем данные.")
            clear_player_data()
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

load_player_data()