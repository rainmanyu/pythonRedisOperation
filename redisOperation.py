import redis
import json

r = redis.Redis(host='10.2.16.113', port=6379, db=9)
# redis = redis.Redis(host='35.235.36.138', port=6379, db=1)


def write_site(key, operator_info):
    b_return = r.set(key, json.dumps(operator_info))
    return b_return


def delete_site(key):
    b_rtn = r.delete(key)
    return b_rtn


def read_site(key):
    json_str = r.get(key)
    if json_str is not None:
        return json.loads(json_str)
    else:
        return None


def read_sites():
    json_rtn = json.loads("{}")
    json_rtn.update({"code": 1})

    json_list = json.loads("{}")

    operator_list = []
    for element in r.mget(r.keys()):
        element_object = json.loads(element)
        operator_list.append(element_object)

    json_list.update({"list": operator_list})
    return json_list


def delete_all():
    r.flushall()
    # for elem in r.keys():
    #     r.delete(elem)

