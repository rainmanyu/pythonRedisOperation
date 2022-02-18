import json
import redisOperation
import httpUtils.getVersion
import config.constants as c
import logging
import time
import timeit
import jsonUtil


def baseurl(fullurl, key):
    pos = fullurl.find(key)
    return fullurl[0:pos - 1]


def rename_domain_key(key):
    if redisOperation.read_site(key) is not None:
        key = key + "_1"
    else:
        key = key

    return key


def update_version(element, base, path, tag_name, deploy_time_name):
    version_json = httpUtils.getVersion.http_get(base, path)
    if not httpUtils.getVersion.is_error_response(version_json):
        element.update({tag_name: version_json['tag']})
        element.update({deploy_time_name: version_json['deployTime']})
    else:
        logging.error("update error. domainId: %s, operator name: %s ", element['domainId'], element['operatorName'])
        element.update({tag_name: 'not_ready'})
        element.update({deploy_time_name: 'not_ready'})


def parse_json(json_content):
    for element in json_content['list']:
        # set playerAPI base url
        player_base = baseurl(element['playerAPI'], 'v1/player/')
        element.update({"player_base": player_base})

        # add casino version
        update_version(element, player_base,
                       c.c_player_version_path,
                       c.c_redis_key_player_version_tag,
                       c.c_redis_key_player_version_deploy_time)

        # set casinoAPI base url
        casino_base = baseurl(element['casinoAPI'], 'v1/casino/')
        element.update({"casino-base": casino_base})

        # add casino version
        update_version(element, casino_base,
                       c.c_casino_version_path,
                       c.c_redis_key_casino_version_tag,
                       c.c_redis_key_casino_version_deploy_time)

        # add FE, the default value
        element.update({c.c_redis_key_frontend: c.c_frontend_src_em})

        # rename duplicate id
        key = rename_domain_key(str(element['domainId']))
        redisOperation.write_site(key, element)


def correct_env(env):
    if env.lower().find('stage') != -1:
        env = 'stage'
    elif env.lower().find('prod') != -1:
        env = 'production'
    else:
        env = env + '_error'

    return env


def update_site(element):
    # set playerAPI base url
    player_base = baseurl(element['playerAPI'], 'v1/player/')
    element.update({"player_base": player_base})

    # add casino version
    update_version(element, player_base,
                   c.c_player_version_path,
                   c.c_redis_key_player_version_tag,
                   c.c_redis_key_player_version_deploy_time)

    # set casinoAPI base url
    casino_base = baseurl(element['casinoAPI'], 'v1/casino/')
    element.update({"casino-base": casino_base})

    # add casino version
    update_version(element, casino_base,
                   c.c_casino_version_path,
                   c.c_redis_key_casino_version_tag,
                   c.c_redis_key_casino_version_deploy_time)

    # update time
    element.update({c.c_redis_key_update_time: time.ctime()})

    # update env
    # element.update({'environment': correct_env(element['environment'])})
    # element.update({'k': element['domainId']})
    # print(element['key'])
    # if not (element['key'] is None):
    #     if element['domainId'] != element['key']:
    #         element.update({'status': 'error'})
    # else:
    #     element.update({'key': element['domainId']})


def update_versions():
    logging.info("Update sites version starts : %s ", time.ctime())
    start = timeit.default_timer()
    sites = redisOperation.read_sites()
    for element in sites['list']:
        update_site(element)
        redisOperation.write_site(element['domainId'], element)
    stop = timeit.default_timer()
    spent_time = stop - start
    logging.info("Update sites version ends. total spent time : %s ", spent_time)
    logging.info("")
    logging.info("")
    logging.info("")
    logging.info("")
    return spent_time


def update_site_tag(key):
    logging.info("Update site version starts : %s ", time.ctime())
    start = timeit.default_timer()
    site = redisOperation.read_site(key)
    if site is not None:
        update_site(site)
        redisOperation.write_site(key, site)
        stop = timeit.default_timer()
        spent_time = stop - start

        logging.info("Update site tag ends. key: %s total spent time : %s , write redis status:", key, spent_time)
        logging.info("")
        logging.info("")
        logging.info("")
        logging.info("")

        return spent_time
    else:
        logging.error("site is None, key:" + key)
        return None


def get_valid_value(value):
    if value is not None:
        return value
    else:
        return ""


def parse_sites_json(sites):
    json_info = '{}'
    json_obj = json.loads(json_info)
    for element in sites:
        json_obj.update({c.c_redis_key_operator_group: get_valid_value(element[c.c_json_key_operator_group])})
        json_obj.update({c.c_redis_key_operator: get_valid_value(element[c.c_json_key_operator])})
        json_obj.update({c.c_redis_key_domain_id: get_valid_value(element[c.c_json_key_domain_id])})
        json_obj.update({c.c_redis_key_gm_core_env: get_valid_value(element[c.c_json_key_gm_core_env])})
        json_obj.update({c.c_redis_key_partner_id: get_valid_value(element[c.c_json_key_partner_id])})

        json_obj.update({c.c_redis_key_partner_key: get_valid_value(element[c.c_json_key_partner_key])})
        json_obj.update({c.c_redis_key_environment: get_valid_value(element[c.c_json_key_environment])})
        json_obj.update({c.c_redis_key_frontend: get_valid_value(element[c.c_json_key_frontend])})
        json_obj.update({c.c_redis_key_region: get_valid_value(element[c.c_json_key_region])})
        json_obj.update({c.c_redis_key_status: get_valid_value(element[c.c_json_key_status])})

        json_obj.update({c.c_redis_key_player_api: get_valid_value(element[c.c_json_key_player_api])})
        json_obj.update({c.c_redis_key_casino_api: get_valid_value(element[c.c_json_key_casino_api])})
        json_obj.update({c.c_redis_key_live_lobby: get_valid_value(element[c.c_json_key_live_lobby])})
        json_obj.update({c.c_redis_key_gic: get_valid_value(element[c.c_json_key_gic])})
        json_obj.update({c.c_redis_key_notification: get_valid_value(element[c.c_json_key_notification])})

        json_obj.update({c.c_redis_key_balance_updates: get_valid_value(element[c.c_json_key_balance_updates])})

        json_obj.update({c.c_redis_key_casino_base: c.c_not_ready})
        json_obj.update({c.c_redis_key_casino_version_tag: c.c_not_ready})
        json_obj.update({c.c_redis_key_casino_version_deploy_time: c.c_not_ready})

        json_obj.update({c.c_redis_key_player_base: c.c_not_ready})
        json_obj.update({c.c_redis_key_player_version_tag: c.c_not_ready})
        json_obj.update({c.c_redis_key_player_version_deploy_time: c.c_not_ready})

        json_obj.update({c.c_redis_key_update_time: c.c_not_ready})

        key = str(element[c.c_json_key_domain_id])
        print(key)
        while redisOperation.read_site(key) is not None:
            key = jsonUtil.rename_domain_key(key)
        json_obj.update({c.c_redis_key_key: str(key)})
        w_rtn = redisOperation.write_site(str(key), json_obj)
        print(w_rtn)
    print('finish writing all site')
