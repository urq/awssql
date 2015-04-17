import json

from boto.ec2.elb import LoadBalancer
from boto.ec2.autoscale import AutoScalingGroup
from boto.ec2.instance import Instance


ORM = {
    "instances": Instance,
    "elbs": LoadBalancer,
    "asgs": AutoScalingGroup
}

def get_schema(table):
    table_obj = ORM.get(table, None)
    if not table_obj:
        return None
    orm_obj = table_obj()
    attrs = {a_id: str for a_id in dir(orm_obj)
             if not (callable(getattr(orm_obj, a_id)) or a_id.startswith("_"))}
    return attrs

def get_types(table, items):
    schema = get_schema(table)
    for item in items:
        for field in schema:
            best_type = getattr(item, field)
            if best_type:
                best_type = type(best_type)
            if best_type:
                schema[field] = best_type
    return schema

