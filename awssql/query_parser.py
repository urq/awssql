import sqlparse
from sqlparse.sql import Identifier


# This example illustrates how to extract table names from nested
# SELECT statements.

# See:
# http://groups.google.com/group/sqlparse/browse_thread/thread/b0bd9a022e9d4895


def extract_tables(sql):
    select = sqlparse.parse(sql)[0]
    potential_tables = [tid.value for tid in select.tokens if isinstance(tid,
                                                                         sqlparse.sql.Identifier)]
    return [t for t in potential_tables if "." not in t]


def show_tables(query):
    return extract_tables(query)
