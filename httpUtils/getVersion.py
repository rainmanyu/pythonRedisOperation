import http.client
import json
from json import JSONDecodeError
import logging


def http_get(url, path):
    try:
        if not url:
            conn = http.client.HTTPSConnection(url)
            conn.request("GET", path)
            r1 = conn.getresponse()
            data1 = r1.read()  # This will return entire content.
            return json.loads(data1)
        else:
            return json.loads('{"error":"OtherError"}')
    except ConnectionRefusedError:
        print(url + path)
        return json.loads('{"error":"ConnectionRefusedError"}')
    except JSONDecodeError:
        print(url + path)
        return json.loads('{"error":"JSONDecodeError"}')
    else:
        return json.loads('{"error":"OtherError"}')


def is_error_response(response_json):
    return "error" in response_json

# http_get("https://hizlicasino.nwacdn.com", "/v1/casino/versionInfo")
# http_get('https://tipico-games-api.prod.norway.everymatrix.com', '/v1/casino/versionInfo')
