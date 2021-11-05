# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from common.settings import SQLITE_PATH, SQLITE_NAME
from views import app

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:{SQLITE_PATH}/{SQLITE_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class SqlClient:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def add(self, *args, **kwargs):
        global obj
        if len(args) > 0 and isinstance(*args, list):
            for dict in args[0]:
                obj = self(**dict)
                db.session.add(obj)
        else:
            obj = self(**kwargs)
            db.session.add(obj)
        db.session.commit()
        return obj

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
