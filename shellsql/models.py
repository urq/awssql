import re
from csv import DictReader, DictWriter

from .utils import get_headers

class Dataset(object):
    def __init__(self, key=None, headers=None, data=None):
        self.headers = headers
        self.data = data
        self.key = key

    def write(self, fd, delim='\t'):
        writer = DictWriter(fd, self.headers, delimiter=delim)
        writer.writeheader()
        for row in self.data:
            writer.writerow(row)

    @classmethod
    def from_file(cls, fd, delim='\t'):
        reader = DictReader(fd, delimiter=delim)
        data = [row for row in reader]
        headers = data[0].keys() if len(data) > 0 else None
        return cls(headers=headers, data=data)

    def merge(self, other_dataset):
        return Dataset(headers=set(self.headers + other_dataset.headers),
                       data=(self.data + other_dataset.data))

    def map(self, transform):
        def dict_update(row, extra):
            row.update(extra)
            return row
        data = [dict_update(row, transform(row)) for row in self.data]
        return Dataset(headers=get_headers(data), data=data)

    def filter(self, predicate):
        data = [row for row in self.data if predicate(row)]
        return Dataset(headers=get_headers(data), data=data)

    def select(self, columns):
        col_spec = self._select_columns(columns)
        headers = [header for i, header in enumerate(self.headers)
                   if i in col_spec or header in col_spec]
        data = [{header:row[header] for header in headers} for row in self.data]
        return Dataset(headers=headers, data=data)

    def group_by(self, columns):
        # return GroupedDataset(groups)
        pass #returns GroupedDataset

    def agg(self, agg_func):
        return agg_func(self.data)

    def _select_columns(self, columns):
        """Given a list of string representations of columns, returns a set of integers
        representing each column.

        >>> d = Dataset(headers=['this', 'that'])
        >>> d._select_columns('1-3')
        set(1, 2, 3)
        >>> d._select_columns('1-3,8-12')
        set(1, 2, 3, 8, 9, 10, 11, 12)
        >>> d._select_columns('that')
        set(1)
        >>> d._select_columns('this,that')
        set(0, 1)
        """
        if isinstance(columns, basestring):
            columns = [columns]
        col_spec = set()
        for col in columns:
            if col.startswith('-') or col[0] in '0123456789':
                m = re.match(r'(?P<first>[0-9]*)-(?P<last>[0-9]*)', col)
                first = int(m.group('first')) if m.group('first') else 0
                last = int(m.group('last')) if m.group('last') else len(self.headers)
                col_spec |= set(range(first, last))
            else:
                col_spec.add(col)
        return col_spec

class GroupedDataset(object):
    def __init__(self, groups):
        self.groups = groups

    def agg(self, agg_func):
        pass
        #return [group.agg(agg_func) for group in self.groups]



# def test_parse():
    # test_cases = [
            # '1-3',
            # '1-magic',
            # 'a-c',
            # '1-3,5-7'
        # ]
    # for test in test_cases:
        # print test, parse(test)

#number = d+
#range = number|(number?-number?)
#name = [a-zA-Z0-9_-]+
#term = (name|range)
#statement = term(,term)*
    #from pyparsing import *
    #dash = Literal('-')
    #lodash = Literal('_')
    #comma = Literal(',')
    #number = Word(nums)
    #range_ = number | Combine(Optional(number) + dash + Optional(number))
    #name = Word(alphas + nums + '_')
    #term = name | range_
    #statement = term | Combine(term + Optional(Combine(comma + ZeroOrMore(term))))
    #return statement.parseString(string)


        #for x in tmp:
            #y = x.split('-')
            #if len(y) == 0: continue
            #if len(y) == 1: cols.add(int(y[0]))
            #if len(y) == 2: cols.update(range(int(y[0]), int(y[1])+1))
            #if len(y) > 2: raise ValueError("Misformatted columnspec.")
        #return sorted(list(cols))
