#!/usr/bin/env python
# from __future__ import print_function
from collections import defaultdict
from multiprocessing import Pool

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


def load_data_wrapper(args):
    load_data(*args)


def load_data(table, access_key, secret_key):
    data_set = requests.get(table, access_key, secret_key)
    print "{}\n-------".format(table)
    for x in schemas.get_types(table, data_set):
        print x
    print

if __name__ == '__main__':
    _, env, q = sys.argv
    tables = query_parser.extract_tables(q)
    access_key, secret_key = utility.load_keys(env)
    thread_pool = Pool(5)
    thread_pool.map(load_data_wrapper, [(t, access_key, secret_key) for t in tables])


