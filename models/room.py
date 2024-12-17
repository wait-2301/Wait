from datetime import datetime

class Room:
    def __init__(self, id, room_name, status='AVAILABLE'):
        self.id = id
        self.room_name = room_name
        self.status = status
        self.updated_at = datetime.utcnow()