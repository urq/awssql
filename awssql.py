#!/usr/bin/env python
# from __future__ import print_function

import sys
from awssql import cache
from awssql import database as db
from awssql import query_parser
from awssql import requests
from awssql import schemas
from awssql import utility

conn = db.create_db()

def insert_table(conn, tablename, items):
    schema = schemas.get_schema(tablename)
    db.create_table(conn, tablename, schema)
    for item in items:
        db.insert_item(conn, tablename, utility.object_to_tabular(item, schema))
    conn.commit()


def figure_out_type(tablename, items):
    schema = schemas.get_schema(tablename)
    for item in items:
        print utility.object_type(item, schema)


if __name__ == '__main__':
    _, env, q = sys.argv
    # tables = query_parser.extract_tables(q)
    # for t in tables:
    #     figure_out_type(t, requests.get(t, *utility.load_keys(env)))
