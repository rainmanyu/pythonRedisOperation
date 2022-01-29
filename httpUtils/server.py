from flask import Flask, request, Response, jsonify
from flask_cors import CORS

import redisOperation

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/site/<domain_id>')
def get_site_by_domain_id(domain_id):
    return jsonify(redisOperation.read_site(domain_id))


@app.route('/sites')
def get_sites():
    return jsonify(redisOperation.read_sites_new())


if __name__ == '__main__':
    app.run()
