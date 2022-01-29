import redis
import json

r = redis.Redis(host='10.2.16.113', port=6379)


def write_site(domain_id, operator_info):
    r.set(domain_id, json.dumps(operator_info))
    print('finish write domain:' + domain_id)


def read_site(domain_id):
    json_str = r.get(domain_id)

    if json_str is not None:
        return json.loads(json_str)
    else:
        return None


def read_sites_v2():
    sites_list = []
    for elem in r.keys():
        sites_list.append(r.get(elem))
    return json.dumps(sites_list)


def read_sites():
    json_str = '{"code": 1, "data": { "list": ['
    end_str = ' ]}}'
    values_list = r.mget(r.keys())
    for element in values_list:
        print(str(element))
        element_object = json.loads(element)
        json.dumps(element_object)
        json_str = json_str + str(element_object)
        json_str += ','
    json_str = json_str[0:len(json_str) - 1]
    json_str = json_str + end_str
    print(json_str)
    # json_str = json_str.replace('\'', '"')

    #
    # sites_json = json.loads(sites_json_str)
    #
    # values_list = r.mget(r.keys())
    # print(values_list)
    #
    # print(json.loads(values_list))
    # sites_json['data'].update({"list": values_list})
    #
    # # sites_json_str_rtn = json.dumps(sites_json)
    # print(sites_json)
    # # return json.loads(sites_json_str_rtn)
    print(json_str)
    return json.loads(json_str)


def read_sites_new():
    # json_rtn = json.dumps({})
    json_rtn = json.loads("{}")
    json_rtn.update({"code": 1})

    json_list = json.loads("{}")

    operator_list = []
    for element in r.mget(r.keys()):
        element_object = json.loads(element)
        operator_list.append(element_object)

    json_list.update({"list": operator_list})
    return json_list


def get_keys():
    keys = r.keys()
    print(type(keys))
    print(keys)
    print(len(keys))


def delete_all():
    for elem in r.keys():
        r.delete(elem)


read_sites_new()
