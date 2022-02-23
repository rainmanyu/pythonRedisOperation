import json
import traceback
from decimal import Decimal
import json
import logging
from decimal import Decimal

import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

import jsonUtil
import redisOperation

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
            return jsonify({"status": "ok", "spent_time": Decimal(spent_time).quantize(Decimal('0.00'))})
        else:
            logging.info("Manual update failed.")
            return jsonify({"status": "error", "spent_time": Decimal(spent_time).quantize(Decimal('0.00'))})


@app.route('/version_tag/<key>', methods=['PUT'])
def update_site_tag(key):
    logging.info("Update sites version manually")
    flag = False
    spent_time = 0
    error_message = 'Unknown Error'
    try:
        spent_time = jsonUtil.update_site_tag(key)
        if spent_time is not None:
            error_message = ''
            flag = True
        else:
            flag = False
            spent_time = 0
            error_message = 'site not existed. key:' + key
    finally:
        if flag:
            logging.info("Manual update successfully.")
            return jsonify({"status": "ok", "spent_time": Decimal(spent_time).quantize(Decimal('0.00')), "errorMessage": error_message})
        else:
            logging.info("Manual update failed.")
            return jsonify({"status": "error", "spent_time": Decimal(spent_time).quantize(Decimal('0.00')),
                            "errorMessage": error_message})


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            file = request.files['file']
            if file is not None:
                print('start read excel')
                print(file)
                excel_raw_data_1 = pd.read_excel(file, sheet_name='Sheet2')
                print(excel_raw_data_1)
                data_str = excel_raw_data_1.to_json(orient='records')
                print(data_str)
                data_json = json.loads(data_str)
                print(data_json)
                print('clear db')
                redisOperation.delete_all()
                print('parse data')
                jsonUtil.parse_sites_json(data_json)
                print('end')
                return "ok"
        except Exception as ex:
            print(ex)
            traceback.print_exc()
        else:
            print('no error')
        finally:
            print('finally')
    else:
        return "not supported method."


if __name__ == '__main__':
    logging.basicConfig(filename='run.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    app.run(host='0.0.0.0', port=9876)
