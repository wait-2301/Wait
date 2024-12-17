from datetime import datetime

class User:
    def __init__(self, user_id, name, email=None, passwords=None, phone_number=None, telegram_id=None, category='STANDARD'):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.passwords = passwords
        self.phone_number = phone_number
        self.telegram_id = telegram_id
        self.category = category
        self.registered_at = datetime.utcnow()