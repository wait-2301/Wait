class Analytics:
    def __init__(self, user_id, average_wait_time=None, visit_count=0, last_visited_at=None):
        self.user_id = user_id
        self.average_wait_time = average_wait_time
        self.visit_count = visit_count
        self.last_visited_at = last_visited_at