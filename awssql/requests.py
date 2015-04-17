import boto

def get_instances(access_key, secret_key):
    ec2_conn = boto.connect_ec2(access_key, secret_key)
    return [i for res in ec2_conn.get_all_reservations() for i in res.instances]


def get_elbs(access_key, secret_key):
    elb_conn = boto.connect_elb(access_key, secret_key)
    return [x for x in elb_conn.get_all_load_balancers()]


def get_asgs(access_key, secret_key):
    asg_conn = boto.connect_autoscale(access_key, secret_key)
    return [x for x in asg_conn.get_all_groups()]


LOOK_UP = {
    "instances": get_instances,
    "elbs": get_elbs,
    "asgs": get_asgs
}


def missing(access_key, secret_key):
    return []


def get(t, access_key, secret_key):
    get_fun = LOOK_UP.get(t, missing)
    return get_fun(access_key, secret_key)

