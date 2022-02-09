import json

from flask import Flask, request, Response, jsonify
from flask_cors import CORS

import redisOperation
import timer.timer
import logging

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/site/<domain_id>', methods=['POST', 'GET'])
def get_site_by_domain_id(domain_id):
    if request.method == 'GET':
        return jsonify(redisOperation.read_site(domain_id))
    else:
        data = json.loads(request.get_data(as_text=True))
        b_rtn = redisOperation.write_site(str(data['domainId']), data)
        print(b_rtn)
        return jsonify({"status": "ok"})


@app.route('/sites')
def get_sites():
    return jsonify(redisOperation.read_sites())


if __name__ == '__main__':
    logging.basicConfig(filename='run.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    timer.timer.tl.start(block=False)
    app.run(host='0.0.0.0', port=9888)
