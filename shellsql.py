import os
import pickle
import sys

import click
from shellsql import aws
from shellsql.models import Dataset
from shellsql.cache import TTLCache, FileCache
from shellsql import utils

@click.group()
def cli():
    pass

@cli.command()
def hello():
    click.echo("hello world!")

@cli.command()
@click.argument('columns', nargs=-1)
def select(columns):
    data = Dataset.from_file(sys.stdin)
    data.select(columns).write(sys.stdout)

@cli.command()
def headers():
    print '\n'.join(sorted(Dataset.from_file(sys.stdin).headers))

@cli.command()
@click.option('--region', default='us-east-1')
@click.option('--cache-dir', default='~/.shellsql-cache')
@click.option('--cache-ttl', default=60)
@click.argument('profiles', nargs=-1)
def get(profiles, cache_dir, cache_ttl, region):
    # if not os.path.exists(os.path.expanduser(cache_dir)):
        # os.mkdir(os.path.expanduser(cache_dir))
    # cache = TTLCache(FileCache(os.path.expanduser(cache_dir)))
    # data = cache.get(profile)
    # if data is None:
        # data = aws.get_instances_as_table(profile, region)
        # print 'inserting into cache'
        # cache.insert(profile, pickle.dumps(data))
    # else:
        # data = pickle.loads(data)

    data = reduce(lambda x, y: x.merge(y),
                  [aws.get_instances_as_table(profile, region)
                   for profile in profiles])
    data.write(sys.stdout)

#@cli.command()
#@click.argument('predicate')
#def map(columns, predicate):
    #data = Dataset.from_file(sys.stdin)
    #def func(row): exec predicate + '; return row' in globals(), locals()
    #data = data.map(func)
    #data.write(sys.stdout)

@cli.command()
@click.argument('predicate')
def filter(predicate):
    data = Dataset.from_file(sys.stdin)
    utils.import_execution_env()
    print "predicate: {}".format(predicate)
    func_str = """filter_func = lambda row: {}""".format(predicate)
    print func_str
    exec(func_str)
    data = data.filter(filter_func)
    data.write(sys.stdout)

if __name__ == '__main__':
    cli()
