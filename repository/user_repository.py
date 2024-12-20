from app.db_connect import db_conn
from app.db_exception_handler import handle_db_exception


def insert_user(user_id, phone_number, password_hash, table_number):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (user_id, full_name, category, email, phone_number, passwords) VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, "New Manager", "Менеджер", None, phone_number, password_hash)
        )
        conn.commit()
        print(f"New record inserted in users: {user_id}")
    except Exception as e:
        handle_db_exception(e, "inserting into users")
    finally:
        cur.close()
        conn.close()

def get_user_by_phone_number(phone_number):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(f"""
                SELECT * FROM users 
                WHERE phone_number = '{phone_number}';
            """)
        
        user = cur.fetchone()
    except Exception as e:
        handle_db_exception(e, "selecting user")
    finally:
        cur.close()
        conn.close()
        if user:
            return user
        else:
            return None