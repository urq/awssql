import json

from boto.ec2.instance import Instance

ORM = {
    "instances": Instance
}

def get_schema(table):
    table_obj = ORM.get(table, None)
    if not table_obj:
        return ["Unknown"]
    orm_obj = table_obj()
    attrs = [{"name": a_id, "type": "text"} for a_id in dir(orm_obj)
             if not (callable(getattr(orm_obj, a_id)) or a_id.startswith("_"))]
    return attrs
