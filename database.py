import sqlite3
from sqlite3 import Error
dbname="database.db"
def create_connection(db_file):
    try:
        conn = sqlite3.connect(dbname)
        print("connected")
        return conn
    except Error as e:
        print(e)
        return None

def run_query(sql_query, args=[]):
    conn = create_connection(dbname)
    cur = conn.cursor()
    if sql_query.lower().startswith("select"):
        cur.execute(sql_query, args)
        print("running  "+sql_query)
        return cur.fetchall()
    else:
        cur.execute(sql_query, args)
        print("running  " + sql_query)
    try:
        conn.commit()
    except Exception as e:
        print(e)


def create_tables():
    sql_query = '''create table if not exists website(
    id INTEGER PRIMARY KEY,
    location text,
    temp text,
    description text,
    time TIMESTAMP);
    '''
    run_query(sql_query)
    print("table created")
    #return conn

def insert(location, temp, description, time):
    sql_query = '''INSERT INTO website(location,temp,description,time) values(?,?,?,?)'''
    run_query(sql_query, [location, temp, description, time])
    print("inserted"+location)

def replace(location, temp, description, time):
    sql_query = '''REPLACE INTO website(location,temp,description,time) values(?,?,?,?)'''
    run_query(sql_query, [location, temp, description, time])

def get(location):
    sql_query = """select temp,description,time from website where location = ? """
    return run_query(sql_query, [location])

def delete(location):
    sql_query="""DELETE FROM website WHERE location = ? """
    run_query(sql_query,[location])
