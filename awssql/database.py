
import sqlite3
def create_db():
    """returns an in-memory sqllitedb"""
    return sqlite3.connect(":memory:")

def create_table(conn, table, schema):
    conn.execute('CREATE TABLE %s (%s)' %
        (table, ', '.join("%s %s" % (item['name'], item['type']) for item in schema)))
    conn.commit()
    return conn

def insert_item(conn, table, item):
    prep_query = 'INSERT INTO %s VALUES (%s)' % (table, ','.join('?' for i in range(len(item))))
    conn.execute(prep_query, item)

def query(conn, query):
    c = conn.execute(query)
    return c.fetchall()

