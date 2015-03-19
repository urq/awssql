import boto

def get(resource, creds):
    pass

def get_instances(access_key, secret_key):
    ec2_conn = boto.connect_ec2(access_key, secret_key)
    return [i for res in ec2_conn.get_all_reservations() for i in res.instances]
