import sqlite3

def sql_execute(db_path, query = None, data = None):
    """
    Выполняет SQL-запрос (INSERT, UPDATE, DELETE, CREATE) к базе данных.
    :param db_path: Путь к файлу базы данных.
    :param query: SQL-запрос.
    :param data: Кортеж с параметрами для запроса (по умолчанию None).
    :return: True при успехе, False при ошибке.
    """
    if query:
        try:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                print(query)
                if data:
                    print(data)
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                db.commit()
                return True
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return False
        except Exception as e:  # Другие неожиданные ошибки
            print(f"Unexpected error: {e}")
            return False
    else:
        return False

def sql_select(db_path, query, data=None):
    """Функция для выполнения SELECT запросов"""
    if query:
        try:
            with sqlite3.connect(db_path) as db:
                cursor = db.cursor()
                if data:
                    cursor.execute(query, data)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                print(results)
                return results
        except sqlite3.Error as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    else:
        return None

def db_create(db_path):
    """
    Создаёт таблицу users, если она не существует.
    :param db_path: Путь к базе данных.
    :return: True при успехе, False при ошибке.
    """
    query = """
     CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id BIGINT UNIQUE,
            name TEXT,
            cat1 TEXT,
            cat2 TEXT,
            cat3 TEXT,
            costs1 real,
            costs2 real,
            costs3 real
        )"""
    return sql_execute(db_path,query)

def db_add(db_path, tabel_name, data):
    """
    Добавляет новую запись в таблицу.
    :param db_path: Путь к базе данных.
    :param tabel_name: Имя таблицы.
    :param data: Словарь с данными для вставки.
    :return: True при успехе, False при ошибке.
    """
    columns = ', '.join(data.keys())
    placeholders = ', '.join(['?'] * len(data))
    query = f"INSERT INTO {tabel_name} ({columns}) VALUES ({placeholders})"
    return sql_execute(db_path, query, tuple(data.values()))

def db_update(db_path, tabel_name, data, cond):
    """
    Обновляет запись в таблице по условию.
    :param db_path: Путь к базе данных.
    :param tabel_name: Имя таблицы.
    :param data: Словарь с обновляемыми данными.
    :param cond: Словарь с условиями (например, {'user_id': 123}).
    :return: True при успехе, False при ошибке.
    """
    columns = ', '.join([f"{k} = ?" for k in data.keys()])
    set_values = tuple(data.values())
    cond_str, cond_values = generate_conditions(cond)
    query = f"UPDATE {tabel_name} SET {columns}{cond_str}"
    return sql_execute(db_path, query, set_values + cond_values)

def db_select(db_path, tabel_name = 'users', cond = None,):
    """
    Выполняет SELECT-запрос к таблице с опциональным условием.
    :param db_path: Путь к базе данных.
    :param tabel_name: Имя таблицы.
    :param cond: Словарь с условиями (по умолчанию None).
    :return: Список кортежей с результатами или None при ошибке.
    """
    cond_str, cond_values = generate_conditions(cond)
    query = f"SELECT * FROM {tabel_name}{cond_str}"
    return sql_select(db_path, query, cond_values)

def generate_conditions(cond):
    """
    Генерирует строку условий WHERE для SQL-запроса и кортеж значений.
    :param cond: Словарь условий.
    :return: (строка WHERE, кортеж значений)
    """
    if cond is None:
        return "", tuple()
    condition = " AND ".join([f"{k} = ?" for k in cond.keys()])
    return f" WHERE {condition}", tuple(cond.values())
