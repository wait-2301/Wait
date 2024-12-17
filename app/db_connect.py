import psycopg2


def db_conn():
    return psycopg2.connect(
        dbname='wait',
        user='postgres',
        password='qwerty',   # "1234" or "qwerty"
        host='localhost',
        port='5432'
    )