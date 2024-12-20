from telebot import TeleBot
from functools import wraps
from flask import redirect, session, url_for

def manager_only(is_manager, bot: TeleBot):
    """ensure only managers can call specific commands."""
    def decorator(func):
        def wrapper(message, *args, **kwargs):
            if not is_manager(message.chat.id):
                bot.send_message(message.chat.id, "Вы не имеете доступа к этой команде.")
                return
            return func(message, *args, **kwargs)
        return wrapper
    return decorator




def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))  # Redirect to login page
        return f(*args, **kwargs)
    return decorated_function