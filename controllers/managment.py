from flask import Blueprint, jsonify, render_template, request, session
import services.queue_service as QM
from utils.decorators import login_required

# Create a blueprint
management = Blueprint("management", __name__)
# Данные для очереди
queue = [
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
    {"name": "Космухамбетов Ансар", "time": "", "ticket": "B111"},
    {"name": "Ерке Есхан", "time": "00:05", "ticket": ""},
]


@management.route('/')
@login_required
def queue_list():
    return render_template('managment.html') 


@management.route('/q', methods=['GET'])
@login_required
def queue_by_queue_number():
    queue_number = request.args.get('queue_number')
    if not queue_number:
        return "Не указан номер очереди", 400

    queue_data = QM.get_queue_by_queue_number_service(queue_number)

    # Get the client from the database
    if queue_data is None:
        return "Клиент не найден", 404
    
    room = QM.get_room_by_manager_user_id_service(session.get('user_id'))
    QM.set_room_for_queue_service(queue_data.id, room.id)
    QM.set_status_for_queue(queue_data.id, 'IN_PROGRESS')
    QM.set_room_status_service(room.id, 'OCCUPIED')

    client_info = {
        'name': queue_data.full_name,
        'reason': queue_data.purpose,
        'ticket': queue_data.queue_number,  # Optional, as it seems to be used in another part
        'time': '',   # Optional, in case the client has an appointment time
        'id': queue_data.id,         # Optional, if needed for unique identification
        'table_name': room.room_name
    }

    return render_template('managment2.html', queue_number=queue_number, client_info=client_info)



@management.route('/queue')
def get_all_queue():
    data = QM.get_all_queue_service()
    queue_json = [
        {
            "name": queue_data.full_name,        # full_name
            "time": "",                   # no time provided, set as empty
            "ticket": queue_data.queue_number       # queue_number
        }
        for queue_data in data
    ]
    return jsonify(queue_json)
