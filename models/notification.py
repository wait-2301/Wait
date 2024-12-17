from datetime import datetime

class Notification:
    def __init__(self, user_id, notification_type, message, status='PENDING'):
        self.user_id = user_id
        self.notification_type = notification_type
        self.message = message
        self.status = status
        self.sent_at = datetime.utcnow()