import sys

from boto3.session import Session

from .models import Dataset
from .utils import get_headers

def get_instances_as_table(profile=None, region_name='us-east-1'):

    session = Session(profile_name=profile)
    ec2 = session.resource('ec2')
    data = extract_data_from_objects(ec2.instances.all())
    # enrich data with meta info
    for row in data:
        row.update({'AWSProfile': profile})

    def kf(k):
        """Keep everything under the 'meta.data.' header name.
        Keep the AWSProfile keyname around.
        Throw out everything else.
        """
        prefix = 'meta.data.'
        if k.startswith(prefix):
            return k[len(prefix):]
        if k == 'AWSProfile':
            return k
        return None

    data = clean_data(data, key_filter=kf)
    return Dataset(headers=sorted(get_headers(data)), data=data)

def clean_data(data, key_filter=None, value_filter=None):
    if key_filter is None:
        key_filter = lambda x:x
    if value_filter is None:
        value_filter = lambda x:x

    updated_data = []
    for row in data:
        updated_row = {}
        for k,v in row.iteritems():
            k = key_filter(k)
            if k is None:
                continue
            v = value_filter(v)
            updated_row[k] = v
        updated_data.append(updated_row)
    return updated_data


def extract_data_from_objects(objs):
    """Take in an iterable of objects and extract each object's attributes into
    a dictionary, as long as the attributes don't start with a '_', are callable,
    and aren't themselves iterable.

    :param objs iter[object]: an iterable of python objects
    :rtype: list[dict]
    """
    nested_data = [loop('', obj) for obj in objs]
    return [{x.lstrip('.'):y for x, y in strip_nones(flatten(item))} for item in nested_data]

def strip_nones(l): return (x for x in l if x is not None)

def flatten(l):
    """Flatten an arbitrarily nested list.
    """
    for el in l:
        if isinstance(el, list) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def loop(key, val):
    """These are either class instances or dicts, and we're trying to get their members.
    """
    if hasattr(val, '__dict__'): # convert instance object to a dict
        val = {k:v for k,v in val.__dict__.iteritems() if not k.startswith('_')}
    if isinstance(val, dict):
        return [loop(key + '.' + str(k), v) for k, v in val.iteritems()]
    elif hasattr(val, '__iter__'):
        pass #TODO do something with iterables
    else: # it must be a normal, non-container object
        return (key, val)

