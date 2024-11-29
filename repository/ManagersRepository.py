import psycopg2

from models.Managers import Managers

def db_conn():
    return psycopg2.connect(
        dbname='wait',
        user='postgres',
        password='qwerty',   # "1234" or "qwerty"
        host='localhost',
        port='5432'
    )


def get_all_managers():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM managers;''')
    data = cur.fetchall()
    cur.close()
    conn.close()

    queue = [Managers(id=row[0], user_id=row[1]) for row in data]
    return queue

def get_manager_by_id(id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM managers WHERE id = %s;''', (id))
    queue_data = cur.fetchone()
    cur.close()
    conn.close()

    if queue_data:
        return Managers(id=queue_data[0], user_id=queue_data[1])
    else:
        return None
    
def manager_count_by_user_id(user_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM managers WHERE user_id = %s", (user_id,))
    count = cur.fetchone()[0]
    print("managers count : ", count)

    cur.close()
    conn.close()
    return count

print(manager_count_by_user_id(1167373997))