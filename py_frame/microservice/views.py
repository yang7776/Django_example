# -*- coding: utf-8 -*-
import json

from flask import Flask, request

app = Flask(__name__)


# @app.route("/lizhu/<action>", methods=['GET'])
# def device_info(action):
#     device_func = lambda: (False, {})
#     if action == "Device":
#         from .logic import get_device_info as device_func
#
#     elif action == "System":
#         from .logic import get_system_info as device_func
#
#     elif action == "Version":
#         from .logic import get_version as device_func
#
#     flag, data = device_func()
#     code = 200 if flag is True else 406
#     res = {"code": code, "result": data}
#
#     return json.dumps(res)


@app.route("/lizhu/<action>", defaults={'scene_id': None}, methods=["GET", "POST", "PUT"])
@app.route("/lizhu/<action>/<scene_id>", methods=["GET", "POST", "PUT"])
def agent_files(action, scene_id):
    if request.method == "GET":
        data = request.values.get("key")
        res = {"get_data":data}
    elif request.method == "POST":
        data = request.values.get("key")
        res = {"post_data": data}
    elif request.method == "PUT":
        data = request.values.get("key")
        res = {"put_data": data}
    else:
        res = {""}
    return json.dumps(res)

app.run()