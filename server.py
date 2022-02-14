import json

from flask import Flask, request, Response, jsonify
from flask_cors import CORS

import redisOperation
import logging
import jsonUtil

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/site/<key>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def get_site_by_domain_id(key):
    if request.method == 'GET':
        return jsonify(redisOperation.read_site(key))
    elif request.method == 'PUT':
        # update a site
        data = json.loads(request.get_data(as_text=True))
        b_rtn = redisOperation.write_site(str(data['key']), data)
        return jsonify({"status": "ok", "flag": b_rtn})
    elif request.method == 'POST':
        # new a site
        data = json.loads(request.get_data(as_text=True))
        key = str(data['key'])
        while redisOperation.read_site(key) is not None:
            key = jsonUtil.rename_domain_key(key)
        data['key'] = key
        w_rtn = redisOperation.write_site(str(key), data)
        return jsonify({"status": "ok", "key": key, "flag": w_rtn})
    elif request.method == 'DELETE':
        d_rtn = redisOperation.delete_site(key)
        return jsonify({"status": "ok", "key": key, "flag": d_rtn})


@app.route('/sites')
def get_sites():
    return jsonify(redisOperation.read_sites())


@app.route('/update_version')
def update_version():
    logging.info("Update sites version manually")
    flag = False
    spent_time = 0
    try:
        spent_time = jsonUtil.update_versions()
        flag = True
    finally:
        if flag:
            logging.info("Manual update successfully.")
            return jsonify({"status": "ok", "spent_time": spent_time})
        else:
            logging.info("Manual update failed.")
            return jsonify({"status": "error", "spent_time": spent_time})


if __name__ == '__main__':
    logging.basicConfig(filename='run.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    app.run(host='0.0.0.0', port=9888)
