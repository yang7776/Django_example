# -*- coding: utf-8 -*-
from flask import Flask
app = Flask(__name__)
# app.debug = True

from py_frame.microservice.views import main

app.register_blueprint(main, url_prefix='/lizhu')

def run():
    app.run(port=8000)


