from datetime import datetime

class Manager:
    def __init__(self, user_id, added_by, room_id):
        self.user_id = user_id
        self.added_by = added_by
        self.room_id = room_id
        self.granted_at = datetime.utcnow()