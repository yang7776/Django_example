from flask import Blueprint

import json

main = Blueprint('main', __name__)


@main.route('/index/', methods=['GET'])
def show_index():
    return json.dumps({"code": 200, "result": {"data": "执行成功！"}})
