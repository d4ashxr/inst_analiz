import telebot
from main import connection

# Создание бота с помощью pyTelegramBotAPI
API_TOKEN = '7762465167:AAHgBx10i7YxxFg4BNeLYheK-hVpIzxfCUk'  # Поместите ваш токен в переменные окружения или конфиг файл
bot = telebot.TeleBot(API_TOKEN)

# Сохранение состояния для каждого пользователя
user_data = {}


# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_data.pop(user_id, None)  # Очищаем состояние пользователя, если существует

    bot.reply_to(message,
                 "Привет! Пожалуйста, введи свой логин для Instagram. ⚠️ ВНИМАНИЕ: нельзя использовать бота чаще 1 раза в день. Если у вас включена двухфакторная аутентификация, бот не сможет подключиться.")


# Получаем логин пользователя
@bot.message_handler(func=lambda message: message.text not in ['/start', '/help'])
def get_login(message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {}

    if 'login' not in user_data[user_id]:
        user_data[user_id]['login'] = message.text
        bot.reply_to(message, "Теперь введи свой пароль для Instagram.")
    elif 'password' not in user_data[user_id]:
        user_data[user_id]['password'] = message.text
        bot.reply_to(message, "Попробуем подключиться к твоему аккаунту...")

        username = user_data[user_id]['login']
        password = user_data[user_id]['password']

        result = connection(username, password)

        # Обработка результата
        if isinstance(result, list):
            if len(result) == 6:
                follower_and_not_followee_usernames = [user[0] for user in result[5]]
                followee_and_not_follower_usernames = [user[0] for user in result[4]]

                answ_to_user = (
                    f"✅ Вот данные по вашему аккаунту:\n\n"
                    f"🔢 Количество подписок: {result[0]}\n"
                    f"🔢 Количество подписчиков: {result[1]}\n\n"
                    f"🔁 Подписаны на вас, но вы не подписаны на них: {result[2]}\n"
                    f"🔁 Список таких пользователей: {', '.join(follower_and_not_followee_usernames)}\n\n"
                    f"↔️ Вы подписаны на них, но они не подписаны на вас: {result[3]}\n"
                    f"↔️ Список таких пользователей: {', '.join(followee_and_not_follower_usernames)}"
                )
            elif len(result) == 7:
                if result[-1] == 'finish':
                    new_followers_usernames = [user for user in result[3]]
                    new_followees_usernames = [user for user in result[4]]
                    unfollowed_users_usernames = [user for user in result[5]]

                    answ_to_user = (
                        f"✅ Вот обновленные данные по вашему аккаунту:\n\n"
                        f"🔢 Количество новых подписчиков: {result[0]}\n"
                        f"➕ Список новых подписчиков: {', '.join(new_followers_usernames)}\n\n"
                        f"🔢 Количество новых подписок: {result[1]}\n"
                        f"➕ Список новых пользователей, на которых вы подписались: {', '.join(new_followees_usernames)}\n\n"
                        f"❌ Количество пользователей, которые отписались от вас: {result[2]}\n"
                        f"❌ Список отписавшихся пользователей: {', '.join(unfollowed_users_usernames)}"
                    )
            else:
                answ_to_user = "Неизвестный формат данных!"
        else:
            answ_to_user = f"Ошибка: {result}"

        bot.reply_to(message, answ_to_user)


# Запуск бота
bot.polling(none_stop=True)