# -*- coding: utf-8 -*-
from views import app
from db_operate import db
from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate

manage = Manager(app)
migrate = Migrate(app, db)
manage.add_command('db', MigrateCommand)

if __name__ == '__main__':
    """
    python manage.py db init 初始化数据库

    python manage.py db migrate 迁移数据
    
    python manage.py db upgrade 更新数据库
    """
    manage.run()
