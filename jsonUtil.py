import json
import redisOperation
import httpUtils.getVersion
import config.constants


def baseurl(fullurl, key):
    pos = fullurl.find(key)
    return fullurl[0:pos - 1]


def rename_domain_key(key):
    if redisOperation.read_json(key) is not None:
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
        element.update({tag_name: 'not_ready'})
        element.update({deploy_time_name: 'not_ready'})


def parse_json(json_content):
    for element in json_content['list']:
        # set playerAPI base url
        player_base = baseurl(element['playerAPI'], 'v1/player/')
        element.update({"player-base": player_base})

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
                       config.constants.c_player_version_path,
                       config.constants.c_player_version_tag,
                       config.constants.c_player_version_deploy_time)

        # add FE, the default value
        element.update({config.constants.c_frontend_tag: config.constants.c_frontend_src_em})

        # rename duplicate id
        key = rename_domain_key(str(element['domainId']))
        redisOperation.write_json(key, element)
