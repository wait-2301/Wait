import repository.queue_history_repository as qhr


def get_all_history_service():
    return qhr.get_all_queue_history()

def save_queue_history(queue, action, manager_id):
    qhr.insert_into_queue(queue, action, manager_id)