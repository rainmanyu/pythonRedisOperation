import redis
import json

r = redis.Redis(host='10.2.16.113', port=6379)


def write_json(domain_id, operator_info):
    r.set(domain_id, json.dumps(operator_info))


def read_json(domain_id):
    json_str = r.get(domain_id)

    if json_str is not None:
        return json.loads(json_str)
    else:
        return None


def get_keys():
    keys = r.keys()
    print(type(keys))
    print(keys)
    print(len(keys))


def delete_all():
    for elem in r.keys():
        r.delete(elem)


# get_keys()

