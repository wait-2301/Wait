from datetime import datetime

class User:
    def __init__(self, user_id, name, category, passwords, phone_number, email=None, telegram_id=None):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.passwords = passwords
        self.phone_number = phone_number
        self.telegram_id = telegram_id
        self.category = category
        self.registered_at = datetime.utcnow()