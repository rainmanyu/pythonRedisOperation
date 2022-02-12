import json
import redisOperation
import httpUtils.getVersion
import config.constants
import logging
import time
import timeit


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
                       config.constants.c_player_version_path,
                       config.constants.c_player_version_tag,
                       config.constants.c_player_version_deploy_time)

        # set casinoAPI base url
        casino_base = baseurl(element['casinoAPI'], 'v1/casino/')
        element.update({"casino-base": casino_base})

        # add casino version
        update_version(element, casino_base,
                       config.constants.c_casino_version_path,
                       config.constants.c_casino_version_tag,
                       config.constants.c_casino_version_deploy_time)

        # add FE, the default value
        element.update({config.constants.c_frontend_tag: config.constants.c_frontend_src_em})

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
                   config.constants.c_player_version_path,
                   config.constants.c_player_version_tag,
                   config.constants.c_player_version_deploy_time)

    # set casinoAPI base url
    casino_base = baseurl(element['casinoAPI'], 'v1/casino/')
    element.update({"casino-base": casino_base})

    # add casino version
    update_version(element, casino_base,
                   config.constants.c_casino_version_path,
                   config.constants.c_casino_version_tag,
                   config.constants.c_casino_version_deploy_time)

    # update time
    element.update({config.constants.c_update_time: time.ctime()})

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
