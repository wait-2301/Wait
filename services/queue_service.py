import repository.queue_repository as qr
import repository.managers_repository as mr
import repository.room_repository as rr

from prettytable import PrettyTable



def get_all_queue_service():
    return qr.get_all_queue()

def get_queue_count_by_user_id_service(user_id):
    return qr.queue_count_by_user_id(user_id)

def get_queue_by_id_service(id):
    return qr.get_queue_by_id(id)

def get_queue_by_user_id_service(user_id):
    return qr.get_queue_by_user_id(user_id)

def get_queue_by_queue_number_service(queue_number):
    return qr.get_queue_by_queue_number(queue_number)

def insert_into_queue_service(user_id, name, room, purpose):
    qr.insert_into_queue(user_id, name, room, purpose)

def get_user_queue_number_service(user_id):
    return qr.get_user_queue_number(user_id)

def delete_user_from_queue_service(user_id):
    qr.delete_user_from_queue(user_id)

def delete_queue_entry_by_id(entry_id):
    qr.delete_queue_entry_by_id(entry_id)

def get_all_queue_entries_table():
    queue = qr.get_all_queue_entries()

    if not queue:
        return "Очередь пуста."
    else:
        table = PrettyTable()
        table.field_names = ["#", "Имя и Фамилия", "Номер Стола", "Цель Визита", "Лгота", "Статус"]

        for queue_number, full_name, room_id, purpose, priority, status in queue:
            room_name = None
            if room_id:
                room_name = rr.get_room_name_by_id(room_id)
                room_name = room_name[0] if isinstance(room_name, tuple) else room_name  # Extract string from tuple if needed
            room_name = room_name[:10] if room_name else "Не назначено"     
            priority_text = "Да" if priority else "Нет"
            table.add_row([
            queue_number,
            full_name[:30],  # Truncate to fit table width
            room_name,       # Already truncated or default text
            purpose[:30],    # Truncate to fit table width
            priority_text,
            status[:11]      # Truncate to fit table width
            ])

        return f"```{table}```"
    
def get_first_queue():
    return qr.get_first_queue_entry()

def set_room_for_queue_service(queue_id, room_id):
    qr.set_room_for_queue(queue_id, room_id) 

def set_status_for_queue(queue_id, status):
    qr.set_status_for_queue(queue_id, status)



def get_all_managers_service():
    return mr.get_all_managers()

def get_manager_by_id_service(id):
    return mr.get_manager_by_id(id)

def is_manager(user_id):
    count = mr.manager_count_by_user_id(user_id)
    return count > 0

def get_managers_with_rooms_service():
    return mr.get_managers_with_rooms()

def get_managers_with_rooms_table():
    managers = mr.get_managers_with_rooms()  # Fetches managers and their rooms from the database

    if not managers:
        return "Нет менеджеров или комнаты не назначены."
    else:
        table = PrettyTable()
        table.field_names = ["#", "ID Менеджера", "Кем Добавлен", "Когда Назначено", "Стол"]

        for idx, (manager_id, user_id, added_by, granted_at, room_name) in enumerate(managers, start=1):
            room_name = room_name[:10] if room_name else "Не назначено"  # Truncate room name to fit table
            table.add_row([
                idx,                               # Row number for display
                user_id,                           # User ID of the manager
                str(added_by)[:10] if added_by else "Не указано",  # Convert int to str, then truncate
                str(granted_at)[:10] if granted_at else "Не указано",  # Date when manager was granted
                room_name                          # Room name or default text
            ])
        
        return f"```{table}```"

def get_room_id_by_manager_user_id_service(user_id):
    return mr.get_room_id_by_manager_user_id(user_id)

def add_manager_by_user_id_service(user_id, added_by, room_id):
    print("Calling add_manager_by_user_id() for : ", user_id)
    mr.add_manager_by_user_id(user_id, added_by, room_id)

def remove_manager_service(manager_id):
    print("Calling remove_manager() for : ", manager_id)
    mr.remove_manager(manager_id)    



def get_available_room_name_service():
    room = rr.get_available_room_name()
    return room

def set_room_status_service(room_id, status):
    rr.set_room_status(room_id, status)

def get_unassigned_rooms_service():
    return rr.get_available_rooms_for_managers()

from prettytable import PrettyTable

def get_unassigned_rooms_table_service():
    unassigned_rooms = rr.get_available_rooms_for_managers()  # Fetch available rooms
    if not unassigned_rooms:
        return "Нет доступных кабинетов."
    else:
        # Create a table
        table = PrettyTable()
        table.field_names = ["#", "Название Стола", "Статус"]

        # Iterate over the unassigned rooms, accessing Room attributes
        for idx, room in enumerate(unassigned_rooms, start=1):
            table.add_row([
                idx,                # Row number
                room.room_name[:10] if room.room_name else "Не указано",  # Truncate room name if too long
                room.status         # Room status
            ])
        
        return f"```{table}```"


def get_room_name_by_id_service(id):
    return rr.get_room_name_by_id(id)

def get_room_by_manager_user_id_service(user_id):
    return rr.get_room_by_manager_user_id(user_id)

def get_room_id_by_room_name_service(room_name):
    return rr.get_room_id_by_room_name(room_name)
    

    
   

