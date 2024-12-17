from app.db_connect import db_conn
from models.queue_history import QueueHistory
from app.db_exception_handler import handle_db_exception

def get_all_queue_history():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute("SELECT * FROM queue_history;")
        data = cur.fetchall()
        print("All queue : ", data)
    except Exception as e:
        handle_db_exception(e, "fetching all queues")
    finally:
        cur.close()
        conn.close()

    history = [QueueHistory(id=queue_history[0], timestamp=queue_history[1], action=queue_history[2],
                   queue=queue_history[3], manager_id=queue_history[4]) for queue_history in data]
    return history


def insert_into_queue(queue, action, manager_id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO queue_history (action, queue, manager_id) VALUES (%s, %s, %s)",
            (action, queue, manager_id)
        )
        conn.commit()
        print(f"New record inserted in queue_history: {queue}")
    except Exception as e:
        handle_db_exception(e, "inserting into queue_history")
    finally:
        cur.close()
        conn.close()