import telebot
import psycopg2
from threading import Timer
import os
from dotenv import load_dotenv
import services.QueueService as qm


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

db_conn = psycopg2.connect(
    dbname='wait',
    user='postgres',
    password='qwerty',   # "1234" or "qwerty"
    host='localhost',
    port='5432'
)
db_conn.autocommit = True

# bot = telebot.TeleBot('7610327249:AAHFW8oNcFzu2HCuz5zH2Kcj0Xl0G00_8Ms')
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

current_applicant = None
applicant_timer = None
DEFAULT_TIMER_SECONDS = 120

def is_manager(user_id):
    print("USER COUNT BY ", user_id, " = ", qm.get_managers_count_by_user_id_service(user_id))
    count = qm.get_managers_count_by_user_id_service(user_id)

    return count > 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в систему электронной очереди! 🕒\n"
        "Доступные команды:\n"
        "/register - Зарегистрироваться в очереди\n"
        "/status - Проверить статус очереди\n"
        "/leave - Покинуть очередь\n"
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

    users_count = qm.get_queue_count_by_user_id_service(user_id)
    if users_count > 0:
        bot.send_message(user_id, "Вы уже зарегистрированы в очереди! ✅")
    else:
        bot.send_message(user_id, "Укажите номер кабинета или место:")
        bot.register_next_step_handler(message, lambda msg: get_registration_details(msg, user_name))


def get_registration_details(message, user_name):
    user_id = message.chat.id
    room = message.text
    bot.send_message(user_id, "Укажите цель визита:")
    bot.register_next_step_handler(message, lambda msg: finalize_registration(msg, user_name, room))

def finalize_registration(message, user_name, room):
    user_id = message.chat.id
    purpose = message.text

    position = qm.get_next_position_service()
    qm.insert_into_queue_service(user_id, user_name, room, purpose, position)

    bot.send_message(
        user_id,
        f"Вы успешно зарегистрированы!\n"
        f"Ваш номер: {position}\n"
        f"Имя: {user_name}\n"
        f"Кабинет: {room}\n"
        f"Цель: {purpose}"
    )

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.chat.id
    result = qm.get_user_position_service(user_id)

    if result:
        bot.send_message(user_id, f"Ваш текущий номер в очереди: {result[0]}")
    else:
        bot.send_message(user_id, "Вы не зарегистрированы в очереди. Используйте /register.")



@bot.message_handler(commands=['leave'])
def leave_queue(message):
    user_id = message.chat.id
    qm.delete_user_from_queue_service(user_id)
    bot.send_message(user_id, "Вы успешно покинули очередь.")

@bot.message_handler(commands=['queue_list'])
def queue_list(message):
    if not is_manager(message.chat.id):
        bot.send_message(message.chat.id, "Вы не имеете доступа к этой команде.")
        return

    queue = qm.get_all_queue_entries_service()
    bot.send_message(message.chat.id, queue)


@bot.message_handler(commands=['call_next'])
def call_next(message):
    global current_applicant, applicant_timer

    if applicant_timer:
        applicant_timer.cancel()

    with db_conn.cursor() as cur:
        cur.execute("SELECT * FROM queue ORDER BY position LIMIT 1")
        applicant = cur.fetchone()
        if applicant:
            current_applicant = applicant[1]  # user_id
            cur.execute("DELETE FROM queue WHERE id = %s", (applicant[0],))
            bot.send_message(current_applicant, "Ваш черёд! Подойдите, пожалуйста.")
            bot.send_message(
                message.chat.id,
                f"Вызван {applicant[2]}. У него 2 минуты, чтобы подойти."
            )
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
    else:
        bot.send_message(message.chat.id, "Нет активного разговора.")


@bot.message_handler(commands=['no_show'])
def no_show(message):
    global current_applicant, applicant_timer

    if current_applicant:
        bot.send_message(current_applicant, "Вы не подошли вовремя. Очередь движется дальше.")
        current_applicant = None

    if applicant_timer:
        applicant_timer.cancel()

    call_next(message)

@bot.message_handler(commands=['add_manager'])
def add_manager(message):
    if not is_manager(message.chat.id):
        bot.send_message(message.chat.id, "Вы не имеете доступа к этой команде.")
        return

    bot.send_message(message.chat.id, "Укажите ID нового менеджера:")
    bot.register_next_step_handler(message, add_manager_handler)


def add_manager_handler(message):
    try:
        new_manager_id = int(message.text)
        with db_conn.cursor() as cur:
            cur.execute("""
                INSERT INTO managers (user_id) 
                VALUES (%s) 
                ON CONFLICT (user_id) DO NOTHING
            """, (new_manager_id,))

        bot.send_message(message.chat.id, f"Пользователь с ID {new_manager_id} добавлен как менеджер.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID.")

@bot.message_handler(commands=['remove_manager'])
def remove_manager(message):
    if not is_manager(message.chat.id):
        bot.send_message(message.chat.id, "Вы не имеете доступа к этой команде.")
        return

    bot.send_message(message.chat.id, "Укажите ID менеджера для удаления:")
    bot.register_next_step_handler(message, remove_manager_handler)




def remove_manager_handler(message):
    try:
        manager_id = int(message.text)
        with db_conn.cursor() as cur:
            cur.execute("DELETE FROM managers WHERE user_id = %s", (manager_id,))
        bot.send_message(message.chat.id, f"Пользователь с ID {manager_id} удалён из списка менеджеров.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID.")

def move_queue_due_to_no_show():
    global current_applicant
    if current_applicant:
        bot.send_message(current_applicant, "Вы не подошли вовремя. Очередь движется дальше.")
        current_applicant = None

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
