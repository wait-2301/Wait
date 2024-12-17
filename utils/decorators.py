from telebot import TeleBot

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
