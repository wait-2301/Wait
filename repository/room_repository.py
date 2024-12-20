from app.db_connect import db_conn
from models.room import Room
from app.db_exception_handler import handle_db_exception



def get_available_room_name():
    """Fetches the first available room."""
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('''SELECT id, room_name FROM rooms WHERE status = 'AVAILABLE' LIMIT 1;''')
        room = cur.fetchone()
        print("Available room: ", room)
    except Exception as e:
        handle_db_exception(e, "fetching available room")
    finally:
        cur.close()
        conn.close()

    if room:
        return Room(id=room[0], room_name=room[1])
    else:
        return None


def get_room_name_by_id(id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT room_name FROM rooms WHERE id = %s", (id,))
        room_name = cur.fetchone()
        print("Room name by ID: ", room_name)
    except Exception as e:
        handle_db_exception(e, "fetching room name by ID")
    finally:
        cur.close()
        conn.close()

    return room_name[0] if room_name else None


def get_available_rooms_for_managers():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM rooms r
            WHERE NOT EXISTS (
                SELECT 1
                FROM managers m
                WHERE m.room_id = r.id
            )
        """)
        unassigned_rooms = cur.fetchall()

    except Exception as e:
        handle_db_exception(e, "fetching available rooms for managers")
    finally:
        cur.close()
        conn.close()

    if unassigned_rooms:
        return [Room(id=room[0], room_name=room[1], status=room[2]) for room in unassigned_rooms]
    else:
        return None


def set_room_status(room_id, status):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("""
            UPDATE rooms
            SET status = %s, updated_at = NOW()
            WHERE id = %s;
        """, (status, room_id))
        conn.commit()
        print(f"Room {room_id} status updated to {status}.")
    except Exception as e:
        handle_db_exception(e, "setting room status")
    finally:
        cur.close()
        conn.close()


def get_room_by_manager_user_id(user_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(f"""
                    SELECT r.id, r.room_name, r.status
                    FROM rooms r
                    JOIN managers m ON r.id = m.room_id
                    WHERE m.user_id = {user_id};
        """)
        room = cur.fetchone()
    except Exception as e:
        handle_db_exception(e, "fetching manager's room by manager user_id")
    finally:
        cur.close()
        conn.close()

    if room:
        return Room(id=room[0], room_name=room[1], status=room[2])
    else:
        return None
    

def get_room_id_by_room_name(room_name):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(f'''SELECT id FROM rooms WHERE room_name = '{room_name}';''')
        room_id = cur.fetchone()
        print("Room_id is : ", room_id)
    except Exception as e:
        handle_db_exception(e, "fetching room_id by room_name from the rooms table")
    finally:
        cur.close()
        conn.close()

    if room_id:
        return room_id
    else:
        return None
