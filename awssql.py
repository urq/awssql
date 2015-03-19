#!/usr/bin/env python

import sys
from awssql import cache
from awssql import database as db
from awssql import query_parser
from awssql import requests
from awssql import schemas
from awssql import utility

def insert_instances(instances):
    tablename = 'instances'
    conn = db.create_db()
    db.create_table(conn, tablename, schemas.INSTANCE)
    for instance in instances:
        db.insert_item(conn, tablename, utility.object_to_tabular(instance, schemas.INSTANCE))
    conn.commit()
    return conn

if __name__ == '__main__':
    _, env, q = sys.argv
    conn = insert_instances(requests.get_instances(*utility.load_keys(env)))
    utility.format_table(db.query(conn, q))
