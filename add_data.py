import psycopg2
from psycopg2 import OperationalError
import datetime as dt


def add_user_data(username, password, followers, followees):
    # Извлечение имен подписчиков и подписок
    my_list_followers = [f.username for f in followers]
    my_list_followees = [f.username for f in followees]

    update_date = dt.datetime.now()

    account_id = None

    try:
        conn = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="6936",
            database="inst_accaunts",
            port=5432,
        )

        with conn.cursor() as cursor:
            try:
                # Вставляем аккаунт
                query1 = "INSERT INTO ACCOUNTS (username, password) VALUES (%s, %s) RETURNING id"
                cursor.execute(query1, (username, password))

                # Получаем account_id
                account_id = cursor.fetchone()[0]

                # Вставляем подписчиков
                followers_insert_query = (
                    "INSERT INTO followers (account_id, username, update_date) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
                )
                for username in my_list_followers:
                    cursor.execute(followers_insert_query, (account_id, username, update_date))

                # Вставляем подписки
                followees_insert_query = (
                    "INSERT INTO followees (account_id, username, update_date) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
                )
                for username in my_list_followees:
                    cursor.execute(followees_insert_query, (account_id, username, update_date))

                # Подтверждаем транзакцию
                conn.commit()

            except Exception as insert_error:
                print(f"Ошибка вставки в базу данных: {insert_error}")
                conn.rollback()
                raise  # Переброс исключения выше

            # Поиск подписчиков, не являющихся подписками, и наоборот
            cursor.execute(
                "SELECT username FROM followers WHERE account_id = %s "
                "EXCEPT SELECT username FROM followees WHERE account_id = %s",
                (account_id, account_id)
            )
            follower_and_not_followee = cursor.fetchall()

            cursor.execute(
                "SELECT username FROM followees WHERE account_id = %s "
                "EXCEPT SELECT username FROM followers WHERE account_id = %s",
                (account_id, account_id)
            )
            followee_and_not_follower = cursor.fetchall()

            followee_and_not_follower_count = len(followee_and_not_follower)
            follower_and_not_followee_count = len(follower_and_not_followee)
            print(f'на вас не подписаны в ответ:{followee_and_not_follower_count} аккаунтов')
            for i in followee_and_not_follower:
                print(*i)
            print(f'вы не подписаны в ответ на:{follower_and_not_followee_count} аккаунтов')
            for i in follower_and_not_followee:
                print(*i)
            return [
                len(my_list_followees), len(my_list_followers),
                follower_and_not_followee_count,
                followee_and_not_follower_count,
                followee_and_not_follower,
                follower_and_not_followee,
            ]

    except OperationalError as conn_error:
        print(f"Ошибка подключения к базе данных: {conn_error}")
    finally:
        if conn:
            conn.close()
