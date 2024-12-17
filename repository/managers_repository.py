from app.db_connect import db_conn
from models.manager import Manager
from app.db_exception_handler import handle_db_exception


def get_all_managers():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM managers;')
        data = cur.fetchall()
        return [Manager(id=row[0], user_id=row[1], room_id=row[3]) for row in data]
    except Exception as e:
        handle_db_exception(e, "fetching all managers")
    finally:
        cur.close()
        conn.close()


def get_manager_by_id(id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM managers WHERE id = %s;', (id,))
        queue_data = cur.fetchone()
        if queue_data:
            return Manager(id=queue_data[0], user_id=queue_data[1], room_id=queue_data[3])
    except Exception as e:
        handle_db_exception(e, "fetching manager by ID")
    finally:
        cur.close()
        conn.close()
    return None


def manager_count_by_user_id(user_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM managers WHERE user_id = %s', (user_id,))
        count = cur.fetchone()[0]
        print("Managers count: ", count)
        return count
    except Exception as e:
        handle_db_exception(e, "counting managers by user ID")
    finally:
        cur.close()
        conn.close()


def add_manager_by_user_id(user_id, added_by, room_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO managers (user_id, added_by, room_id) 
            VALUES (%s, %s, %s) 
            ON CONFLICT (user_id) DO NOTHING
        """, (user_id, added_by, room_id))
        conn.commit()
    except Exception as e:
        handle_db_exception(e, "adding manager by user ID")
    finally:
        cur.close()
        conn.close()


def remove_manager(manager_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('DELETE FROM managers WHERE user_id = %s', (manager_id,))
        conn.commit()
    except Exception as e:
        handle_db_exception(e, "removing manager")
    finally:
        cur.close()
        conn.close()


def get_managers_with_rooms():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("""
            SELECT m.id, m.user_id, m.added_by, m.granted_at, r.room_name
            FROM managers m
            LEFT JOIN rooms r ON m.room_id = r.id
        """)
        return cur.fetchall()
    except Exception as e:
        handle_db_exception(e, "fetching managers with rooms")
    finally:
        cur.close()
        conn.close()

def get_room_id_by_manager_user_id(user_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(f"""SELECT room_id FROM managers WHERE user_id = {user_id};""")
        return cur.fetchone()
    except Exception as e:
        handle_db_exception(e, "fetching manager's room_id")
    finally:
        cur.close()
        conn.close()
