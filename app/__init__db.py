import psycopg2


db_conn = psycopg2.connect(
    dbname='wait',
    user='postgres',
    password='qwerty',   # "1234" or "qwerty"
    host='localhost',
    port='5432'
)

cur = db_conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS queue (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            name TEXT NOT NULL,
            room TEXT NOT NULL,
            purpose TEXT NOT NULL,
            position INTEGER NOT NULL
    );
        ''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS managers (
        id SERIAL PRIMARY KEY,
        user_id BIGINT UNIQUE
    );
        ''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS change_log (
        id SERIAL PRIMARY KEY,
        table_name TEXT,
        action_type TEXT,
        old_data JSONB,
        new_data JSONB,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
        ''')

cur.execute('''
    INSERT INTO managers(user_id) VALUES (%s), (%s)
''', (5206245464, 1167373997))

db_conn.commit()

cur.execute("SELECT COUNT(*) FROM managers;")
managers_count = cur.fetchone()[0]
print("Managers Count in DB : ", managers_count)


cur.close()
db_conn.close()

      
    