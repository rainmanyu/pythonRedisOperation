import json
import redisOperation
import jsonUtil


def load_file(filename):
    with open(filename, 'r') as jsonfile:
        json_string_rtn = json.load(jsonfile)
        print(type(json_string_rtn))
        return json_string_rtn


print('Start to delete all existed data.')
redisOperation.delete_all()

print('load data from file.')
json_string = load_file('datafile')
print('Loaded json string:')
print(json_string)

print('Start to parse:')
jsonUtil.parse_json(json_string)
print('End.')
