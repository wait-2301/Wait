from app.db_exception_handler import handle_db_exception
from app.db_connect import db_conn
from models.employee import Employee

def get_all_employee():
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.employee_view;')
        data = cur.fetchall()
        return [Employee(user_id=row[0], first_name=row[1], last_name=row[2], position=row[3], table_name=row[4], phone=row[5]) for row in data]
    except Exception as e:
        handle_db_exception(e, "fetching all employee")
    finally:
        cur.close()
        conn.close()


def get_employee_by_id(id):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.employee_view WHERE user_id = %s;', (id,))
        row = cur.fetchone()
        if row:
            return Employee(user_id=row[0], first_name=row[1], last_name=row[2], position=row[3], table_name=row[4], phone=row[5], password_hash=row[6])
    except Exception as e:
        handle_db_exception(e, "fetching employee by ID")
    finally:
        cur.close()
        conn.close()
    return None


def get_employee_by_phone(phone):
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM public.employee_view WHERE phone = %s;', (phone,))
        row = cur.fetchone()
        if row:
            return Employee(user_id=row[0], first_name=row[1], last_name=row[2], position=row[3], table_name=row[4], phone=row[5])
    except Exception as e:
        handle_db_exception(e, "fetching employee by phone")
    finally:
        cur.close()
        conn.close()
    return None