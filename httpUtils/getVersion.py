import http.client
import json
from json import JSONDecodeError


def http_get(url, path):
    try:
        conn = http.client.HTTPSConnection(url.replace("https://", ""));
        conn.request("GET", path)
        r1 = conn.getresponse()
        data1 = r1.read()  # This will return entire content.
        return json.loads(data1)
    except ConnectionRefusedError:
        print(url + path)
        return json.loads('{"error":"ConnectionRefusedError"}')
    except JSONDecodeError:
        print(url + path)
        return json.loads('{"error":"JSONDecodeError"}')
    else:
        print(url + path)
        return json.loads('{"error":"OtherError"}')


def is_error_response(response_json):
    return "error" in response_json

# http_get("https://hizlicasino.nwacdn.com", "/v1/casino/versionInfo")
# http_get('https://tipico-games-api.prod.norway.everymatrix.com', '/v1/casino/versionInfo')
