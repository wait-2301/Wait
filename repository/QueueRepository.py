import psycopg2

from models.Queue import Queue

def db_conn():
    return psycopg2.connect(
        dbname='wait',
        user='postgres',
        password='qwerty',   # "1234" or "qwerty"
        host='localhost',
        port='5432'
    )


def get_all_queue():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM queue;''')
    data = cur.fetchall()
    cur.close()
    conn.close()

    queue = [Queue(id=row[0], user_id=row[1], name=row[2], room=row[3], purpose=row[4], position=row[5]) for row in data]
    return queue

def get_queue_by_id(id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT * FROM queue WHERE id = %s;''', (id))
    queue_data = cur.fetchone()
    cur.close()
    conn.close()

    if queue_data:
        return Queue(id=queue_data[0], user_id=queue_data[1], name=queue_data[2], room=queue_data[3], purpose=queue_data[4], position=queue_data[5])
    else:
        return None
    
def queue_count_by_user_id(user_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM queue WHERE user_id = %s", (user_id,))
    count = cur.fetchone()[0]

    cur.close()
    conn.close()
    return count


def get_next_position():
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''SELECT COALESCE(MAX(position), 0) + 1 FROM queue;''')
    next_position = cur.fetchone()[0] 
    
    cur.close()
    conn.close()
    print("Next position:::: ", next_position)
    
    return next_position

def insert_into_queue(user_id, name, room, purpose, position):
    conn = db_conn()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO queue (user_id, name, room, purpose, position) VALUES (%s, %s, %s, %s, %s)",
        (user_id, name, room, purpose, position)
    )

    conn.commit()
    cur.close()
    conn.close()

    print(f"New record inserted with position: {position}")

def get_user_position(user_id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute("SELECT position FROM queue WHERE user_id = %s", (user_id,))

    cur.close()
    conn.close()

    position = cur.fetchone()
    return position



def delete_user_from_queue(user_id):
    conn = db_conn()
    cur = conn.cursor()   
    cur.execute("DELETE FROM queue WHERE user_id = %s", (user_id,))
    conn.commit()
    cur.close()
    conn.close()

    print(f"User with user_id {user_id} has been removed from the queue.")



def get_all_queue_entries():
    conn = db_conn()
    cur = conn.cursor()  
    cur.execute('''SELECT position, name, room, purpose FROM queue ORDER BY position''')
    data = cur.fetchall()
    cur.close()
    conn.close()

    return data







    



