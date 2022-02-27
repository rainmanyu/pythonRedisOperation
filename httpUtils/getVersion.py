import http.client
import json
from json import JSONDecodeError
import logging
import traceback
import config.constants as c


def http_get(url, path):
    try:
        if not url:
            return c.c_default_version_info_url_empty
        else:
            url = url.replace("https://", "")
            url = url.replace("http://", "")
            conn = http.client.HTTPSConnection(url)
            conn.request("GET", path)
            response = conn.getresponse()
            if response.getcode() == 200:
                data = response.read()
                return json.loads(data)
            else:
                return c.c_default_version_info_404_url_not_found
    except Exception as ex:
        print('exception happened. url:' + (url+path))
        print(ex)
        traceback.print_exc()
        return json.loads('{"error":"exception"}')


def is_error_response(response_json):
    return "error" in response_json

# http_get("https://hizlicasino.nwacdn.com", "/v1/casino/versionInfo")
# http_get('https://tipico-games-api.prod.norway.everymatrix.com', '/v1/casino/versionInfo')
