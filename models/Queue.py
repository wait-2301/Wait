from datetime import datetime

class Queue:
    def __init__(self, id, user_id, queue_number, full_name, room_id=None, purpose=None, priority=False, status='WAITING', created_at=None):
        self.id = id
        self.user_id = user_id
        self.queue_number = queue_number
        self.room_id = room_id
        self.purpose = purpose
        self.priority = priority
        self.status = status
        self.full_name = full_name
        self.created_at = created_at



    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "queue_number": self.queue_number,
            "room_id": self.room_id,
            "purpose": self.purpose,
            "priority": self.priority,
            "status": self.status,
            "full_name": self.full_name,
            "created_at":  self.created_at
        }
    

    def __str__(self):
        return f"Queue(id={self.id}, user_id={self.user_id}, queue_number={self.queue_number}, full_name={self.full_name}, status={self.status})"