import redis
import json

r = redis.Redis(host='10.2.16.113', port=6379)


def write_site(domain_id, operator_info):
    b_return = r.set(domain_id, json.dumps(operator_info))
    print('finish write domain:' + domain_id)
    return b_return


def read_site(domain_id):
    json_str = r.get(domain_id)

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
    for elem in r.keys():
        r.delete(elem)
