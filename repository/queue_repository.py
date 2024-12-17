from app.db_connect import db_conn
from models.queue import Queue
from app.db_exception_handler import handle_db_exception



def get_all_queue():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM queue;")
        data = cur.fetchall()
        print("All queue : ", data)
    except Exception as e:
        handle_db_exception(e, "fetching all queues")
    finally:
        cur.close()
        conn.close()

    queue = [Queue(id=queue_data[0], user_id=queue_data[1], queue_number=queue_data[2],
                   room_id=queue_data[3], purpose=queue_data[4], priority=queue_data[5], 
                   status=queue_data[6], full_name=queue_data[8]) for queue_data in data]
    return queue


def get_queue_by_id(id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM queue WHERE id = %s", (id,))
        queue_data = cur.fetchone()
    except Exception as e:
        handle_db_exception(e, "fetching queue by ID")
    finally:
        cur.close()
        conn.close()

    if queue_data:
        return Queue(id=queue_data[0], user_id=queue_data[1], queue_number=queue_data[2],
                     room_id=queue_data[3], purpose=queue_data[4], priority=queue_data[5],
                     status=queue_data[6], full_name=queue_data[8])
    return None


def get_queue_by_user_id(user_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM queue WHERE user_id = %s", (user_id,))
        queue_data = cur.fetchone()
        print("Queue by user_id : ", queue_data)
    except Exception as e:
        handle_db_exception(e, "fetching queue by user ID")
    finally:
        cur.close()
        conn.close()

    if queue_data:
        return Queue(id=queue_data[0], user_id=queue_data[1], queue_number=queue_data[2],
                     room_id=queue_data[3], purpose=queue_data[4], priority=queue_data[5],
                     status=queue_data[6], full_name=queue_data[8])
    return None


def get_queue_by_queue_number(queue_number):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM queue WHERE queue_number = %s", (queue_number,))
        queue_data = cur.fetchone()
    except Exception as e:
        handle_db_exception(e, "fetching queue by ID")
    finally:
        cur.close()
        conn.close()

    if queue_data:
        return Queue(id=queue_data[0], user_id=queue_data[1], queue_number=queue_data[2],
                     room_id=queue_data[3], purpose=queue_data[4], priority=queue_data[5],
                     status=queue_data[6], full_name=queue_data[8])
    return None


def queue_count_by_user_id(user_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM queue WHERE user_id = %s", (user_id,))
        count = cur.fetchone()[0]
    except Exception as e:
        handle_db_exception(e, "counting queues by user ID")
    finally:
        cur.close()
        conn.close()
    return count


def insert_into_queue(user_id, full_name, room_id, purpose):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO queue (user_id, full_name, room_id, purpose) VALUES (%s, %s, %s, %s)",
            (user_id, full_name, room_id, purpose)
        )
        conn.commit()
        print(f"New record inserted with position: {full_name}")
    except Exception as e:
        handle_db_exception(e, "inserting into queue")
    finally:
        cur.close()
        conn.close()


def get_user_queue_number(user_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT queue_number FROM queue WHERE user_id = %s", (user_id,))
        queue_number = cur.fetchone()
        print("Queue number : ", queue_number)
    except Exception as e:
        handle_db_exception(e, "fetching user queue number")
    finally:
        cur.close()
        conn.close()

    return queue_number


def delete_user_from_queue(user_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM queue WHERE user_id = %s", (user_id,))
        conn.commit()
        print(f"User with user_id {user_id} has been removed from the queue.")
    except Exception as e:
        handle_db_exception(e, "deleting user from queue")
    finally:
        cur.close()
        conn.close()


def delete_queue_entry_by_id(entry_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM queue WHERE id = %s", (entry_id,))
        conn.commit()
        print(f"Queue entry with id {entry_id} has been removed.")
    except Exception as e:
        handle_db_exception(e, "deleting queue entry by ID")
    finally:
        cur.close()
        conn.close()


def get_all_queue_entries():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT queue_number, full_name, room_id, purpose, priority, status FROM queue ORDER BY queue_number")
        data = cur.fetchall()
        print("All queue data : ", data)
    except Exception as e:
        handle_db_exception(e, "fetching all queue entries")
    finally:
        cur.close()
        conn.close()

    return data


def get_first_queue_entry():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM queue ORDER BY queue_number LIMIT 1")
        queue_data = cur.fetchone()
    except Exception as e:
        handle_db_exception(e, "fetching first queue entry")
    finally:
        cur.close()
        conn.close()

    if queue_data:
        return Queue(id=queue_data[0], user_id=queue_data[1], queue_number=queue_data[2],
                     room_id=queue_data[3], purpose=queue_data[4], priority=queue_data[5],
                     status=queue_data[6], full_name=queue_data[8])
    return None


def set_room_for_queue(queue_id, room_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE queue SET room_id = %s WHERE id = %s", (room_id, queue_id))
        conn.commit()
    except Exception as e:
        handle_db_exception(e, "setting room for queue")
    finally:
        cur.close()
        conn.close()


def set_status_for_queue(queue_id, status):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE queue SET status = %s WHERE id = %s", (status, queue_id))
        conn.commit()
    except Exception as e:
        handle_db_exception(e, "setting status for queue")
    finally:
        cur.close()
        conn.close()
