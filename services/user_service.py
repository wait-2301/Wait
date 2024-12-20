import repository.user_repository as UR
import services.queue_service as QS

def save_user(user_id, phone_number, password_hash):
    table = QS.get_available_room_name_service()
    UR.insert_user(user_id, phone_number, password_hash, table.room_name)
    QS.add_manager_by_user_id_service(user_id, 1167373997, table.id)



def get_user_by_phone_number_service(phone_number):
    user = UR.get_user_by_phone_number(phone_number)
    print("Check", user)
    return user