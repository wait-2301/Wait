# import psycopg2 
 
# connection = psycopg2.connection ( 
#     dbname = "fffhfdjfhdhdhd", 
#     user = "postgres", 
#     password = "", 
#     host = "localhost", 
#     port = "5432" 
# ) 
 
# cursor = connection.cursor() 
 
# cursor.execute("SELECT first_name || last_name FROM employees WHERE salary BETWEEN 60000 AND 70000 AND hire_date > '2022-01-01'") 
  
import telebot
from telebot import types
from threading import Timer
import time

bot = telebot.TeleBot('7619704061:AAE4SCDk52PWdBNiGNbqpzbAeZEb6B4GD4k')

# Data Structures
queue = []  # List of users in the queue
queue_status = {}  # Details about each user
current_applicant = None  # Currently being served
applicant_timer = None

# Admin/Manager Data
admin_id = 1167373997  # initial admin
managers = set([admin_id])  # Set of manager IDs

# Constants
DEFAULT_TIMER_SECONDS = 120  # 2 minutes for the applicant to show up

# Utility Functions
def is_manager(user_id):
    """Checks if a user is a manager or admin."""
    return user_id in managers

# Command Handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в систему электронной очереди! 🕒\n"
        "Доступные команды:\n"
        "/register - Зарегистрироваться в очереди\n"
        "/status - Проверить статус очереди\n"
        "/help - Помощь"
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Вот список доступных команд:\n"
        "/register - Зарегистрироваться в очереди\n"
        "/status - Проверить статус очереди\n"
        "/leave - Покинуть очередь\n"
        "/help - Справка по командам"
    )
    if is_manager(message.chat.id):
        help_text += (
            "\n\nМенеджерские команды:\n"
            "/call_next - Вызвать следующего человека в очереди\n"
            "/end_conversation - Завершить разговор с текущим человеком\n"
            "/no_show - Пометить текущего человека как неявившегося\n"
            "/queue_list - Посмотреть список очереди\n"
            "/add_manager - Назначить нового менеджера\n"
            "/remove_manager - Удалить менеджера"
        )
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['register'])
def register(message):
    
    bot.send_message(message.chat.id, "Пожалуйста, введите своё имя:")
    bot.register_next_step_handler(message, get_registration_name)


def get_registration_name(message):
    
    user_id = message.chat.id
    user_name = message.text

    if user_id in queue_status:
        bot.send_message(user_id, "Вы уже зарегистрированы в очереди! ✅")
    else:
        queue_status[user_id] = {"name": user_name}
        bot.send_message(user_id, "Укажите номер кабинета или место:")
        bot.register_next_step_handler(message, get_registration_details)


def get_registration_details(message):

    user_id = message.chat.id
    queue_status[user_id]["room"] = message.text

    bot.send_message(user_id, "Укажите цель визита:")
    bot.register_next_step_handler(message, finalize_registration)


def finalize_registration(message):

    user_id = message.chat.id
    user_purpose = message.text

    queue_status[user_id]["purpose"] = user_purpose
    queue.append(user_id)
    queue_status[user_id]["position"] = len(queue)
    bot.send_message(
        user_id,
        f"Вы успешно зарегистрированы!\n"
        f"Ваш номер: {queue_status[user_id]['position']}\n"
        f"Имя: {queue_status[user_id]['name']}\n"
        f"Кабинет: {queue_status[user_id]['room']}\n"
        f"Цель: {queue_status[user_id]['purpose']}"
    )


@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.chat.id
    if user_id in queue_status:
        position = queue_status[user_id]['position']
        bot.send_message(user_id, f"Ваш текущий номер в очереди: {position}")
    else:
        bot.send_message(user_id, "Вы не зарегистрированы в очереди. Используйте /register.")


@bot.message_handler(commands=['leave'])
def leave_queue(message):

    user_id = message.chat.id
    if user_id in queue_status:
        queue.remove(user_id)
        del queue_status[user_id]
        update_queue_positions()
        bot.send_message(user_id, "Вы успешно покинули очередь.")
    else:
        bot.send_message(user_id, "Вы не зарегистрированы в очереди.")


@bot.message_handler(commands=['add_manager'])
def add_manager(message):
    if message.chat.id != admin_id:
        bot.send_message(message.chat.id, "Вы не имеете доступа к этой команде.")
        return

    bot.send_message(message.chat.id, "Укажите ID нового менеджера:")
    bot.register_next_step_handler(message, add_manager_handler)


def add_manager_handler(message):
    try:
        new_manager_id = int(message.text)
        managers.add(new_manager_id)
        bot.send_message(message.chat.id, f"Пользователь с ID {new_manager_id} добавлен как менеджер.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID.")


@bot.message_handler(commands=['remove_manager'])
def remove_manager(message):
    if message.chat.id != admin_id:
        bot.send_message(message.chat.id, "Вы не имеете доступа к этой команде.")
        return

    bot.send_message(message.chat.id, "Укажите ID менеджера для удаления:")
    bot.register_next_step_handler(message, remove_manager_handler)


def remove_manager_handler(message):
    try:
        manager_id = int(message.text)
        if manager_id in managers:
            managers.remove(manager_id)
            bot.send_message(message.chat.id, f"Пользователь с ID {manager_id} удалён из списка менеджеров.")
        else:
            bot.send_message(message.chat.id, "Этот пользователь не является менеджером.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID.")


@bot.message_handler(commands=['queue_list'])
def queue_list(message):
    if not is_manager(message.chat.id):
        bot.send_message(message.chat.id, "Вы не имеете доступа к этой команде.")
        return

    if not queue:
        bot.send_message(message.chat.id, "Очередь пуста.")
        return

    queue_details = "Очередь:\n"
    for idx, user_id in enumerate(queue, start=1):
        user_data = queue_status[user_id]
        queue_details += (
            f"{idx}. Имя: {user_data['name']}, Кабинет: {user_data['room']}, "
            f"Цель: {user_data['purpose']}, ID: {user_id}\n"
        )
    bot.send_message(message.chat.id, queue_details)


@bot.message_handler(commands=['call_next'])
def call_next(message):
    global current_applicant, applicant_timer

    if applicant_timer:
        applicant_timer.cancel()

    if queue:
        current_applicant = queue.pop(0)
        user_data = queue_status.pop(current_applicant)
        bot.send_message(current_applicant, "Ваш черёд! Подойдите, пожалуйста.")
        bot.send_message(
            message.chat.id,
            f"Вызван {user_data['name']}. У него 2 минуты, чтобы подойти."
        )
        # Start the timer
        applicant_timer = Timer(DEFAULT_TIMER_SECONDS, move_queue_due_to_no_show)
        applicant_timer.start()
    else:
        bot.send_message(message.chat.id, "Очередь пуста.")


@bot.message_handler(commands=['end_conversation'])
def end_conversation(message):
    global current_applicant, applicant_timer

    if current_applicant:
        bot.send_message(current_applicant, "Ваше время завершено. Спасибо!")
        current_applicant = None

    if applicant_timer:
        applicant_timer.cancel()

    bot.send_message(message.chat.id, "Конец разговора. Готов к следующему вызову.")


@bot.message_handler(commands=['no_show'])
def no_show(message):
    global current_applicant, applicant_timer

    if current_applicant:
        bot.send_message(current_applicant, "Вы не подошли вовремя. Очередь движется дальше.")
        current_applicant = None

    if applicant_timer:
        applicant_timer.cancel()

    bot.send_message(message.chat.id, "Человек помечен как неявившийся. Вызывается следующий.")
    call_next(message)


def move_queue_due_to_no_show():
    global current_applicant
    if current_applicant:
        bot.send_message(current_applicant, "Вы не подошли вовремя. Очередь движется дальше.")
        current_applicant = None


def update_queue_positions():
    for idx, user_id in enumerate(queue):
        queue_status[user_id]['position'] = idx + 1



if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
