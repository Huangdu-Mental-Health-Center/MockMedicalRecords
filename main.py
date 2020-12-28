import requests
import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import json
from threading import Thread
import base64

app = Flask(__name__)


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


with open("./marshmallow/mock_medical_records/assets/data.json", encoding='utf8') as medical_record_list_json:
    mock_record_list = json.loads(medical_record_list_json.read())

def decode_raw_jwt_and_return_user_id_str(authorization_jwt_raw: str) -> str:
    authorization_jwt = authorization_jwt_raw.split(" ")[1]
    payload_base64_encoded = authorization_jwt.split(".")[1]
    missing_padding = len(payload_base64_encoded) % 4
    if missing_padding:
        payload_base64_encoded += '='* (4 - missing_padding)
    jwt_payload = json.loads(base64.b64decode(payload_base64_encoded).decode('utf-8'))
    return jwt_payload["http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier"]

@app.route('/query_record_by_user_id_and_order_id', methods=['GET'])
def get_record_by_user_id_and_order_id():
    response = {
        "record": None,
        "success": False,
    }
    try:
        authorization_jwt_raw = request.headers.get("Authorization")
        user_id = decode_raw_jwt_and_return_user_id_str(authorization_jwt_raw)
        order_id = request.args.get('order_id')
        for record in mock_record_list["records"]:
            if record["user_id"] == user_id and record["order_id"] == order_id:
                response["record"] = record
        response["success"] = True
    except Exception as e:
        print(e.with_traceback)
        response = {
        "record": None,
        "success": False,
    }
    return response


@app.route('/query_prescription_by_user_id_and_order_id', methods=['GET'])
def get_prescription_by_user_id_and_order_id():
    response = {
        "prescription": None,
        "success": False,
    }
    try:
        authorization_jwt_raw = request.headers.get("Authorization")
        user_id = decode_raw_jwt_and_return_user_id_str(authorization_jwt_raw)
        user_id = decode_raw_jwt_and_return_user_id_str(authorization_jwt_raw)
        order_id = request.args.get('order_id')
        for prescription in mock_record_list["prescriptions"]:
            if prescription["user_id"] == user_id and prescription["order_id"] == order_id:
                response["prescription"] = prescription
        response["success"] = True
    except Exception as e:
        print(e.with_traceback)
        response = {
        "prescription": None,
        "success": False,
    }
    return response

@app.route('/query_record_by_user_id', methods=['GET'])
def get_record_by_user_id():
    response = {
        "records": [],
        "success": False,
    }
    try:
        authorization_jwt_raw = request.headers.get("Authorization")
        user_id = decode_raw_jwt_and_return_user_id_str(authorization_jwt_raw)
        order_id = request.args.get('order_id')
        for record in mock_record_list["records"]:
            if record["user_id"] == user_id:
                response["records"].append(record)
        response["success"] = True
    except Exception as e:
        print(e.with_traceback)
        response = {
        "records": [],
        "success": False,
        "msg": str(e)
    }
    return response


@app.route('/get_prescription_by_user_id', methods=['GET'])
def get_prescription_by_user_id():
    response = {
        "prescriptions": [],
        "success": False,
    }
    try:
        authorization_jwt_raw = request.headers.get("Authorization")
        user_id = decode_raw_jwt_and_return_user_id_str(authorization_jwt_raw)
        order_id = request.args.get('order_id')
        for prescription in mock_record_list["prescriptions"]:
            if prescription["user_id"] == user_id:
                response["prescriptions"].append(prescription)
        response["success"] = True
    except Exception as e:
        print(e.with_traceback)
        response = {
        "prescriptions": [],
        "success": False,
    }
    return response


@app.route('/exit', methods=['GET'])
def to_exit():
    exit()


def main():
    port_num = 16000
    main_server = WSGIServer(('0.0.0.0', port_num), app)
    print("Mock Medical Record:\nThis service will serve at {}\n".format(port_num))
    main_server.serve_forever()


if __name__ == '__main__':
    main()
