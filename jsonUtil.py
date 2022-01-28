import json
import redisOperation


def baseurl(fullurl, key):
    pos = fullurl.find(key)
    return fullurl[0:pos]


def rename_domain_key(key):
    if redisOperation.read_json(key) is not None:
        key = key + "_1"
    else:
        key = key

    return key


def parse_json(json_content):
    for element in json_content['list']:
        player_base = baseurl(element['playerAPI'], 'v1/player/')
        element.update({"player-base": player_base})
        casino_base = baseurl(element['casinoAPI'], 'v1/casino/')
        element.update({"casino-base": casino_base})

        key = rename_domain_key(str(element['domainId']))
        redisOperation.write_json(key, element)


with open('datafile', 'r') as jsonfile:
    json_string = json.load(jsonfile)

print(type(json_string))
parse_json(json_string)
# print(type(result))
