import instaloader
from add_data import add_user_data
import time
from refresh_data import refresh_user_data
import requests
import os


def read_from_file(filename):
    # Открываем файл в режиме чтения ('r')
    with open(filename, 'r', encoding='utf-8') as file:
        # Читаем все строки из файла и очищаем от пробелов в начале и конце
        lines = [line.strip() for line in file.readlines()]
    return lines

def write_to_file(filename, data):
    # Открываем файл в режиме записи ('w')
    with open(filename, 'w', encoding='utf-8') as file:
        # Проходимся по данным и записываем каждую строку в файл
        for line in data:
            file.write(line + '\n')


def connection(username, password):
    L = instaloader.Instaloader()
    session_file = 'session-' + username

    try:
        session_file_path = f'/var/folders/ks/hc8y2b3d7y157y_6xj6dr8nh0000gn/t/.instaloader-{username}/session-{username}'

        # Проверяем, существует ли файл сессии
        if os.path.exists(session_file_path):
            L.load_session_from_file(username)
            print("Сессия загружена из файла.")
        else:
            print("Файл сессии не найден, требуется новая авторизация.")
            L.login(username, password)
            L.save_session_to_file()  # Сохраняем сессию для дальнейшего использования

        # После успешного логина получаем данные
        profile = instaloader.Profile.from_username(L.context, username)
        print(f"Получаем данные профиля для {username}...")

        print(f"Получаем список подписчиков...")
        time.sleep(2)
        followers = set(profile.get_followers())

        print(f"Получаем список подписок...")
        time.sleep(2)
        followees = set(profile.get_followees())

        if username in read_from_file('accs.txt'):
            return refresh_user_data(username, followers, followees)
        else:
            result = add_user_data(username, password, followers, followees)
            write_to_file('accs.txt', [username])
            return result

    except FileNotFoundError as e:
        return f"Файл сессии не найден: {e}. Попробуйте залогиниться заново."

    except instaloader.exceptions.LoginException as e:
        return f'Необходима повторная авторизация. Попробуйте авторизоваться через браузер: {str(e)}'

    except instaloader.exceptions.InstaloaderException as e:
        return f'Произошла ошибка: {e}'

    except requests.exceptions.ReadTimeout:
        return f'Произошла ошибка ReadTimeout'
    except requests.exceptions.ConnectTimeout:
        return f'Произошла ошибка ConnectTimeout'