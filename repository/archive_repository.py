from app.db_exception_handler import handle_db_exception
from app.db_connect import db_conn


def get_archive():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT queue_status_json FROM queue_status_view;')
        data = cur.fetchone()[0]
    except Exception as e:
        handle_db_exception(e, "fetching archive")
    finally:
        cur.close()
        conn.close()
    if data:
        return data
    else:
        return None
