import sqlite3
from app.core.config import settings

def get_db_connection():
    """
    Создает и возвращает подключение к базе данных.
    """
    db_path = settings.DATABASE_URL.replace("sqlite:///", "")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row #Позволяет обращаться по имени, а не по id
    return conn


def init_db():
    """
    Создает таблицу links, если её еще не существует.
    Вызывается один раз при старте приложения.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL-запрос на создание таблицы.
    # IF NOT EXISTS - не выдаст ошибку, если таблица уже есть
    # PRIMARY KEY AUTOINCREMENT - уникальный растущий ID
    # UNIQUE - запрет дубликатов коротких кодов
    # DEFAULT 0 - начальное значение счетчика
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            long_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )
    """)

    # Сохраняем изменения в файле app.db
    conn.commit()
    conn.close()
    print("✅ База данных инициализирована успешно")


# Вызываем функцию сразу, чтобы при импорте этого модуля таблица создалась
init_db()