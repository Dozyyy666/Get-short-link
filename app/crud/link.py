import sqlite3
import secrets
import string
from app.database import get_db_connection
from app.core.config import settings


def generate_short_code(length: int) -> str:
    """
    Генерирует случайную строку заданной длины из букв и цифр.
    """
    alphabet = string.ascii_letters + string.digits #a-z, A-Z, 0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def create_link(db_conn: sqlite3.Connection, long_url: str, custom_code: str | None = None) -> dict:
    """
    Создает новую запись в базе данных.
    Возвращает словарь с данными созданной ссылки или выбрасывает ошибку, если код занят.
    """
    cursor = db_conn.cursor()

    short_code = custom_code if custom_code else generate_short_code(settings.SHORT_CODE_LENGTH)

    try:
        cursor.execute(
            "INSERT INTO links (short_sode, long_url, clicks) VALUES (?, ?, ?)",
            (short_code, long_url, 0)
        )
        db_conn.commit()

        #Если успешно - вернуть данные в виде словаря
        return {
            "short_code": short_code,
            "long_url": long_url,
            "clicks": 0,
        }

    except sqlite3.IntegrityError:
        #Сработает если short_sode уже существует в БД
        raise ValueError(f"Код '{short_code}' уже занят. Пожалуйста, выберите другой.")

def get_link_by_code(db_conn: sqlite3.Connection, short_code: str) -> dict | None:
    """
    Ищет ссылку по короткому коду.
    Возвращает словарь если нашла - иначе None
    """
    cursor = db_conn.cursor()
    cursor.execute(
        "SELECT short_code, long_url, clicks FROM links WHERE short_code = ?",
        (short_code,)
    )
    row = cursor.fetchone()

    if row:
        return dict(row) #преобразуем sqlite3.Row в словарь python
    return None

def increment_clicks(db_conn: sqlite3.Connection, short_code: str):
    cursor = db_conn.cursor()
    cursor.execute(
        "UPDATE links SET clicks = clicks + 1 WHERE short_sode = ?",
        (short_code,)
    )
    db_conn.commit()