import psycopg2
import datetime as dt
from psycopg2 import OperationalError

def refresh_user_data(username, followers, followees):
    new_followers_set = {f.username for f in followers}
    new_followees_set = {f.username for f in followees}

    update_date = dt.datetime.now()
    current_followers_set = set()
    current_followees_set = set()

    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="6936",
            database="inst_accaunts",
            port=5432,
        )

        with conn.cursor() as cursor:
            # Получаем текущие данные из базы
            cursor.execute(
                "SELECT username FROM followers WHERE account_id = (SELECT id FROM accounts WHERE username = %s)",
                (username,)
            )
            current_followers_set = {row[0] for row in cursor.fetchall()}

            cursor.execute(
                "SELECT username FROM followees WHERE account_id = (SELECT id FROM accounts WHERE username = %s)",
                (username,)
            )
            current_followees_set = {row[0] for row in cursor.fetchall()}

            # Находим новых подписчиков и подписки
            new_followers = new_followers_set - current_followers_set
            new_followees = new_followees_set - current_followees_set
            unfollowed_users = current_followers_set - new_followers_set

            new_followers_count = len(new_followers)
            new_followees_count = len(new_followees)
            unfollowed_users_count = len(unfollowed_users)

            # Обновляем базу данных
            # (обновление логики должно быть добавлено здесь, если необходимо)

            # Возвращаем результат
            return [
                new_followers_count,
                new_followees_count,
                unfollowed_users_count,
                new_followers,
                new_followees,
                unfollowed_users,
                'finish'
            ]

    except OperationalError as conn_error:
        print(f"Ошибка подключения к базе данных: {conn_error}")
        return f"Ошибка подключения к базе данных: {conn_error}"
    finally:
        if conn:
            conn.close()