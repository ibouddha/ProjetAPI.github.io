import psycopg2

def connect():
    connection = psycopg2.connect(
        database = "prompt_projet",
        user = "bouddha",
        password = "logyouin",
        host = "localhost"
    )
    cursor = connection.cursor()
    # cursor.close()
    return cursor

