from datetime import datetime

class QueueHistory:
    def __init__(self, id, action, queue, manager_id=None, timestamp=None):
        self.id = id
        self.timestamp = timestamp or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.action = action
        self.queue = queue
        self.manager_id = manager_id

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp,
            'action': self.action,
            'queue': str(self.queue),  # Store the list as a string (or JSON if preferred)
            'manager': self.manager_id
        }

    def __str__(self):
        return f"QueueHistory(id={self.id}, timestamp={self.timestamp}, action={self.action}, queue={self.queue}, manager_id={self.manager_id})"

