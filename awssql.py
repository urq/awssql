#!/usr/bin/env python

import sys
from awssql import cache
from awssql import database as db
from awssql import query_parser
from awssql import requests
from awssql import schemas
from awssql import utility

def insert_table(tablename, items):
    conn = db.create_db()
    schema = schema.get_schema(tablename)
    db.create_table(conn, tablename, schema)
    for item in items:
        db.insert_item(conn, tablename, utility.object_to_tabular(item, ))
    conn.commit()
    return conn

if __name__ == '__main__':
    _, env, q = sys.argv
    for table in
    conn = insert_table(tablename, requests.get_instances(*utility.load_keys(env)))
    utility.format_table(db.query(conn, q))
