# -*- coding: utf-8 -*-
import json

from flask import Flask, request

app = Flask(__name__)


@app.route("/lizhu/<str:action>", methods=['GET'])
def device_info(action):
    device_func = lambda: (False, {})
    if action == "Device":
        from .logic import get_device_info as device_func

    elif action == "System":
        from microservice.logic import get_system_info as device_func

    elif action == "Version":
        from microservice.logic import get_version as device_func

    flag, data = device_func()
    code = 200 if flag is True else 406
    res = {"code": code, "result": data}

    return json.dumps(res)


@app.route("/lizhu/<str:type>", defaults={'scene_id': None}, methods=["GET", "POST"])
@app.route("/lizhu/<str:type>/<int:scene_id>", methods=["GET", "POST"])
def agent_files(type, scene_id):
    print(type, scene_id)
