import sys

def import_execution_env():
    import re

def flattenjson(j, null_array=False, delim='.'):
    """Take a dict representing a JSON structure and return a table row, having
    converted the nested dictionaries to new fields and the nested arrays to,
    optionally, NULL or a string of the array. Defaults to nulling the array.
    """
    output = {}

    def inner(k, v):
        if isinstance(v, dict):
            for k2, v2 in v.items():
                inner(k + delim + k2, v2)
        elif isinstance(v, list):
            output.update({k: "<redacted_list>" if null_array else str(v)})
        else: # is a terminal value
            output.update({k: v})

    for k, v in j.items():
        inner(k, v)

    return output

def get_headers(data):
    """Loop through the data and collect any headers.
    :param data list[dict]:
    :rtype: set[str]
    :returns: set of headers
    """
    return {k for row in data for k, _ in row.iteritems()} if data is not None else None
