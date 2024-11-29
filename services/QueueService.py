import repository.QueueRepository as qr
import repository.ManagersRepository as mr



def get_all_queue_service():
    return qr.get_all_queue()

def get_queue_count_by_user_id_service(user_id):
    return qr.queue_count_by_user_id(user_id)

def get_queue_by_id_service(id):
    return qr.get_queue_by_id(id)

def get_next_position_service():
    return qr.get_next_position()

def insert_into_queue_service(user_id, name, room, purpose, position):
    qr.insert_into_queue(user_id, name, room, purpose, position)

def get_user_position_service(user_id):
    return qr.get_user_position(user_id)

def delete_user_from_queue_service(user_id):
    qr.delete_user_from_queue(user_id)

def get_all_queue_entries_service():
    queue = qr.get_all_queue_entries()

    if not queue:
        return "Очередь пуста."
    else:
        queue_entries = "Очередь:\n"
        for pos, name, room, purpose in queue:
            queue_entries += f"{pos}. Имя: {name}, Кабинет: {room}, Цель: {purpose}\n"
        return queue_entries



def get_all_managers_service():
    return mr.get_all_managers()

def get_manager_by_id_service(id):
    return mr.get_manager_by_id(id)

def get_managers_count_by_user_id_service(user_id):
    return mr.manager_count_by_user_id(user_id)

