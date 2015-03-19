import os
from ConfigParser import ConfigParser

def object_to_tabular(item, schema):
    #type_map = {"text": str, "integer": int}
    #return [type_map[field['type']](item.__getattribute__(field['name'])) for field in schema]
    return [str(item.__getattribute__(field['name'])) for field in schema]

def format_table(results):
    for row in results:
        print '\t'.join(str(x) for x in row)

def load_keys(env):
    default_key_path = '~/.aws/config'
    env = env.lower()
    conf = ConfigParser()
    config_file = open(os.path.expanduser(default_key_path))
    conf.readfp(config_file)
    access_key = conf.get("profile %s" % env, "aws_access_key_id")
    secret_key = conf.get("profile %s" % env, "aws_secret_access_key")
    config_file.close()
    return (access_key, secret_key)
