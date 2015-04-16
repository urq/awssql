#! /usr/bin/env python
from awssql import schemas
from awssql import utility
from awssql import requests


def gen_schema(table):
    return schemas.get_schema(table)


def get_types(table):
    schema = gen_schema(table)
    items = requests.get(table, *utility.load_keys("vpc"))
    for item in items:
        for field in schema:
            best_type = getattr(item, field)
            if best_type:
                best_type = type(best_type)
            if best_type:
                schema[field] = best_type
    return schema


def analyze(table):
    print "create table {} ({})".format(table,
                                        ",\n".join(["{} {}".format(col, "text")
                                                    for col, val in get_types(table).iteritems()
                                                    if not issubclass(val, list)]))
    linked_tables = {col: val for col, val in get_types(table).iteritems() if issubclass(val, list)}
    print

    for t_name in linked_tables:
        print "create table {0}_{1} ({0} text,\n {1} text)".format(table.rstrip('s'),
                                                                   t_name.rstrip('s'))

if __name__ == '__main__':
    analyze("elbs")
    print
    analyze("instances")
    print
    analyze("asgs")