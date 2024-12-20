import telebot
from telebot import types
from threading import Timer, Lock
import os
from dotenv import load_dotenv
import services.queue_service as qm
from services.queue_service import is_manager

from utils.decorators import manager_only

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Thread-safe storage for manager-specific data
managers_data = {}
lock = Lock()
DEFAULT_TIMER_SECONDS = 180

MESSAGE_ALREADY_REGISTERED = "Вы уже зарегистрированы в очереди! ✅"


CALLBACK_REGISTER = "register"
CALLBACK_STATUS = "status"
CALLBACK_LEAVE = "leave"
CALLBACK_HELP = "help"
CALLBACK_QUEUE_LIST = "queue_list"
CALLBACK_CALL_NEXT = "call_next"
CALLBACK_CALL_NEXT_BY_ID = "call_next_by_id"
CALLBACK_END_CONVERSATION = "end_conversation"
CALLBACK_NO_SHOW = "no_show"
CALLBACK_MANAGERS_LIST = "managers_list"
CALLBACK_ADD_MANAGER = "add_manager"
CALLBACK_REMOVE_MANAGER = "remove_manager"


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):

    action = call.data
    
    if action == CALLBACK_REGISTER:
        bot.answer_callback_query(call.id, text="Регистрация...")
        register(call.message)
    elif action == CALLBACK_STATUS:
        bot.answer_callback_query(call.id, text="Проверка статуса...")
        status(call.message)
    elif action == CALLBACK_LEAVE:
        bot.answer_callback_query(call.id, text="Выход из очереди...")
        leave_queue(call.message)
    elif action == CALLBACK_HELP:
        bot.answer_callback_query(call.id, text="Загрузка справки...")
        help_command(call.message)    
    elif action == CALLBACK_QUEUE_LIST:
        bot.answer_callback_query(call.id, text="Загрузка списка очереди...")
        queue_list(call.message)
    elif action == CALLBACK_CALL_NEXT:
        bot.answer_callback_query(call.id, text="Вызов следующего...")
        call_next_by_default(call.message)
    elif action == CALLBACK_CALL_NEXT_BY_ID:
        bot.answer_callback_query(call.id, text="Вызов по ИД...")
        call_next_by_id(call.message)
    elif action == CALLBACK_END_CONVERSATION:
        bot.answer_callback_query(call.id, text="Завершение разговора...")
        end_conversation(call.message)
    elif action == CALLBACK_NO_SHOW:
        bot.answer_callback_query(call.id, text="Отметка отсутствия...")
        no_show(call.message)
    elif action == CALLBACK_MANAGERS_LIST:
        bot.answer_callback_query(call.id, text="Загрузка списка менеджеров...")
        get_managers_list_table(call.message)
    elif action == CALLBACK_ADD_MANAGER:
        bot.answer_callback_query(call.id, text="Добавление менеджера...")
        add_manager(call.message)
    elif action == CALLBACK_REMOVE_MANAGER:
        bot.answer_callback_query(call.id, text="Удаление менеджера...")
        remove_manager(call.message)


@bot.message_handler(func=lambda message: message.text.lower() in ["start", "/start"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в систему электронной очереди! 🕒\n")
    main_applicant_commnads(message)    
        

def main_applicant_commnads(message):

    button_register = types.InlineKeyboardButton('Зарегистрироваться в очереди', callback_data='register')
    button_status = types.InlineKeyboardButton('Статус очереди', callback_data='status')
    button_leave = types.InlineKeyboardButton('Покинуть очередь', callback_data='leave')
    button_help = types.InlineKeyboardButton('Справка по командам', callback_data='help')

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button_register)
    keyboard.add(button_status)
    keyboard.add(button_leave)
    keyboard.add(button_help)
    bot.send_message(message.chat.id, 
                     text="Доступные команды:\n", reply_markup=keyboard)



@bot.message_handler(func=lambda message: message.text.lower() in ["help", "/help"])
def help_command(message):
    # main_applicant_commnads(message)

    if is_manager(message.chat.id):
       
        button_call_next = types.InlineKeyboardButton('Вызвать следующего', callback_data='call_next')
        button_call_next_by_id = types.InlineKeyboardButton('Вызвать по ID', callback_data='call_next_by_id')
        button_end_conversation = types.InlineKeyboardButton('Завершить разговор', callback_data='end_conversation')
        button_no_show = types.InlineKeyboardButton('Человека неявился', callback_data='no_show')
        button_queue_list = types.InlineKeyboardButton('Список очереди', callback_data='queue_list')
        button_managers_list = types.InlineKeyboardButton('Список менеджеров', callback_data='managers_list')
        button_add_manager = types.InlineKeyboardButton('Назначить нового менеджера', callback_data='add_manager')
        button_remove_manager = types.InlineKeyboardButton('Удалить менеджера', callback_data='remove_manager')

        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(button_call_next)
        keyboard.add(button_call_next_by_id)
        keyboard.add(button_end_conversation)
        keyboard.add(button_no_show)
        keyboard.add(button_queue_list)
        keyboard.add(button_managers_list)
        keyboard.add(button_add_manager)
        keyboard.add(button_remove_manager)

        # bot.send_message(message.chat.id, text='Менеджерские команды:', reply_markup=keyboard)
        bot.send_message(message.chat.id, text='_ Менеджерские команды: _', reply_markup=keyboard, parse_mode="Markdown")
    


@bot.message_handler(func=lambda message: message.text.lower() in ["register", "/register"])
def register(message):
    user_id = message.chat.id
    if is_manager(user_id):
        bot.send_message(message.chat.id, "Вы менеджер. Нажмите на /help чтобы посмотреть на доступные вам команды.")
        return

    users_count = qm.get_queue_count_by_user_id_service(user_id)
    if users_count > 0:
         bot.send_message(user_id, MESSAGE_ALREADY_REGISTERED)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, введите своё имя:")
        bot.register_next_step_handler(message, get_registration_first_name)

def get_registration_first_name(message):
    user_id = message.chat.id
    first_name = message.text
    bot.send_message(user_id, "Пожалуйста, введите своё фамилию:")
    bot.register_next_step_handler(message, lambda msg: get_registration_last_name(msg, first_name))    

def get_registration_last_name(message, first_name):
    user_id = message.chat.id
    full_name = first_name  + " " + message.text
    bot.send_message(user_id, "Укажите цель визита:")
    bot.register_next_step_handler(message, lambda msg: finalize_registration(msg, full_name))

def finalize_registration(message, user_name):
    user_id = message.chat.id
    purpose = message.text

    room_id = None
    qm.insert_into_queue_service(user_id, user_name, room_id, purpose)
    queue = qm.get_queue_by_user_id_service(user_id)
    bot.send_message(
        user_id,
        f"🎉 Вы успешно зарегистрировались в очереди! Ваш номер — {queue.queue_number}. Менеджер вызовет вас по этому номеру."
    )



@bot.message_handler(func=lambda message: message.text.lower() in ["status", "/status"])
def status(message):
    user_id = message.chat.id
    result = qm.get_user_queue_number_service(user_id)

    if is_manager(user_id):
        bot.send_message(message.chat.id, "Вы менеджер. Нажмите на /help чтобы посмотреть на доступные вам команды.")
        return
    if result:
        bot.send_message(user_id, f"Ваш текущий номер в очереди: {result[0]}")
    else:
        bot.send_message(user_id, "Вы не зарегистрированы в очереди. Используйте /register.")



@bot.message_handler(func=lambda message: message.text.lower() in ["leave", "/leave"])
def leave_queue(message):
    user_id = message.chat.id
    delete_user_from_queue(user_id)
    bot.send_message(user_id, "Вы успешно покинули очередь.")



@bot.message_handler(func=lambda message: message.text.lower() in ["queue_list", "/queue_list"])
@manager_only(is_manager, bot)
def queue_list(message):
    queue = qm.get_all_queue_entries_table()
    bot.send_message(message.chat.id, queue, parse_mode="Markdown")


def prompt_for_applicant_id(manager_id, message):
    bot.send_message(manager_id, "Укажите id applicant:")
    bot.register_next_step_handler(message, lambda msg: handle_applicant_id_input(msg, manager_id))

def handle_applicant_id_input(message, manager_id):
    applicant_queue_number = message.text
    applicant_user_id = qm.get_queue_by_queue_number_service(applicant_queue_number).user_id
    call_next(manager_id, applicant_user_id)

def call_next(manager_id, applicant_user_id):
    if not applicant_user_id:
        bot.send_message(manager_id, "Не указан applicant ID.")
        return

    with lock:
        if manager_id not in managers_data:
            managers_data[manager_id] = {"current_applicant": None, "applicant_timer": None}

        manager_data = managers_data[manager_id]
        
        if manager_data["applicant_timer"]:
            manager_data["applicant_timer"].cancel()
        manager_data["current_applicant"] = applicant_user_id
        process_queue_for_applicant(manager_id, applicant_user_id)

        timer = Timer(DEFAULT_TIMER_SECONDS, lambda: move_queue_due_to_no_show(manager_id))
        manager_data["applicant_timer"] = timer
        timer.start()

def process_queue_for_applicant(manager_id, applicant_user_id):
    user_queue = qm.get_queue_by_user_id_service(applicant_user_id)
    room = qm.get_room_by_manager_user_id_service(manager_id)
    qm.set_room_for_queue_service(user_queue.id, room.id)
    qm.set_status_for_queue(user_queue.id, 'IN_PROGRESS')
    qm.set_room_status_service(room.id, 'OCCUPIED')
    notify_applicant_and_manager(user_queue, room, manager_id)

def notify_applicant_and_manager(user_queue, room, manager_id):
    time_in_minutes = int(DEFAULT_TIMER_SECONDS/60)
    bot.send_message(user_queue.user_id, f"Ваш черёд! Подойдите, пожалуйста к столу {room.room_name}. У вас {time_in_minutes} минуты, чтобы подойти.")
    bot.send_message(manager_id, f"Вызван {user_queue.queue_number} на стол {room.room_name}. У него {time_in_minutes} минуты, чтобы подойти.")




@bot.message_handler(func=lambda message: message.text.lower() in ["call_next", "/call_next"])
@manager_only(is_manager, bot)
def call_next_by_default(message):
    manager_id = message.chat.id
    applicant = qm.get_first_queue()
    if applicant:
        call_next(manager_id, applicant.user_id)
    else:
        bot.send_message(manager_id, "Очередь пуста.")



@bot.message_handler(func=lambda message: message.text.lower() in ["call_next_by_id", "/call_next_by_id"])
@manager_only(is_manager, bot)
def call_next_by_id(message):
    manager_id = message.chat.id
    prompt_for_applicant_id(manager_id, message)



@bot.message_handler(func=lambda message: message.text.lower() in ["end_conversation", "/end_conversation"])
@manager_only(is_manager, bot)
def end_conversation(message):
    manager_id = message.chat.id
    with lock:
        if manager_id not in managers_data or not managers_data[manager_id]["current_applicant"]:
            bot.send_message(manager_id, "Нет активного разговора.")
            return
        current_applicant = managers_data[manager_id]["current_applicant"]
        bot.send_message(current_applicant, "Ваше время завершено. Спасибо!")
        queue_id = qm.get_queue_by_user_id_service(current_applicant).id
        qm.set_status_for_queue(queue_id, 'END_CONVERSATION')
        print(qm.get_queue_by_user_id_service(current_applicant))
        delete_user_from_queue(current_applicant)

        managers_data[manager_id]["current_applicant"] = None
        if managers_data[manager_id]["applicant_timer"]:
            managers_data[manager_id]["applicant_timer"].cancel()
        
        bot.send_message(manager_id, "Конец разговора. Готов к следующему вызову.")



@bot.message_handler(func=lambda message: message.text.lower() in ["no_show", "/no_show"])
@manager_only(is_manager, bot)
def no_show(message):
    manager_id = message.chat.id
    with lock:
        if manager_id not in managers_data or not managers_data[manager_id]["current_applicant"]:
            bot.send_message(manager_id, "Нет активного разговора.")
            return
        current_applicant = managers_data[manager_id]["current_applicant"]
        bot.send_message(current_applicant, "Вы не подошли вовремя. Очередь движется дальше. \n Но вы можете снова встать в очередь /register")
        queue_id = qm.get_queue_by_user_id_service(current_applicant).id
        qm.set_status_for_queue(queue_id, 'NO_SHOW')
        delete_user_from_queue(current_applicant)
    

        managers_data[manager_id]["current_applicant"] = None
        if managers_data[manager_id]["applicant_timer"]:
            managers_data[manager_id]["applicant_timer"].cancel()

        bot.send_message(manager_id, "Готов к следующему вызову.")
        

def move_queue_due_to_no_show(manager_id):
    with lock:
        if manager_id in managers_data and managers_data[manager_id]["current_applicant"]:
            current_applicant = managers_data[manager_id]["current_applicant"]
            queue_id = qm.get_queue_by_user_id_service(current_applicant).id
            qm.set_status_for_queue(queue_id, 'NO_SHOW')
            bot.send_message(manager_id, "Апликант не подошол вовремя. Очередь движется дальше.")
            bot.send_message(current_applicant, "Вы не подошли вовремя. Очередь движется дальше.")
            delete_user_from_queue(current_applicant)
            managers_data[manager_id]["current_applicant"] = None



@bot.message_handler(func=lambda message: message.text.lower() in ["managers_list", "/managers_list"])
@manager_only(is_manager, bot)
def get_managers_list_table(message):
    managers = qm.get_managers_with_rooms_table()
    bot.send_message(message.chat.id, managers, parse_mode="Markdown")



@bot.message_handler(func=lambda message: message.text.lower() in ["add_manager", "/add_manager"])
@manager_only(is_manager, bot)
def add_manager(message):
    bot.send_message(message.chat.id, "Укажите ID нового менеджера:")
    bot.register_next_step_handler(message, add_room_for_manager)


def add_room_for_manager(message):
    new_manager_id = str(message.text)
    rooms_table = qm.get_unassigned_rooms_table_service()
    bot.send_message(message.chat.id, "Укажите полное название стола из списка для нового менеджера:")
    bot.send_message(message.chat.id, rooms_table, parse_mode="Markdown")
    bot.register_next_step_handler(message, lambda msg: add_manager_handler(msg, new_manager_id))


def add_manager_handler(message, new_manager_id):
    try:
        new_manager_room_id = qm.get_room_id_by_room_name_service(str(message.text))
        if new_manager_room_id is None:
            bot.send_message(message.chat.id, "Неверное название Стола.")
            return
        qm.add_manager_by_user_id_service(new_manager_id, message.chat.id, new_manager_room_id)
        bot.send_message(message.chat.id, f"Пользователь с ID {new_manager_id} добавлен как менеджер.")
        bot.send_message(new_manager_id, f"Поздравляем вы теперь менеджер.")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID.")


@bot.message_handler(func=lambda message: message.text.lower() in ["remove_manager", "/remove_manager"])
@manager_only(is_manager, bot)
def remove_manager(message):
    bot.send_message(message.chat.id, "Укажите ID менеджера для удаления:")
    bot.register_next_step_handler(message, remove_manager_handler)


def remove_manager_handler(message):
    try:
        manager_id = int(message.text)
        qm.remove_manager_service(manager_id)
        bot.send_message(message.chat.id, f"Пользователь с ID {manager_id} удалён из списка менеджеров.")
        bot.send_message(manager_id, f"Вы более не являетесь менеджером платформы Wait. Благодарим за работу!!!")
    except ValueError:
        bot.send_message(message.chat.id, "Неверный ID.")


def delete_user_from_queue(user_id):
    user_queue = qm.get_queue_by_user_id_service(user_id)
    if user_queue:
        qm.set_room_status_service(user_queue.room_id, 'AVAILABLE')
        qm.delete_user_from_queue_service(user_id)
        print("Deleted!!! ")



# def save_log_in_queue_history(queue, ):


if __name__ == "bot":
    bot.polling(none_stop=True, interval=0)

