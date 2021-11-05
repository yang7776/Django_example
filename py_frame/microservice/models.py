from db_operate import db, SqlClient
from datetime import datetime

STATE = (
    (0, "未执行"),
    (1, "执行成功"),
    (2, "正在执行"),
    (3, "执行失败"),
)


class Task(db.Model, SqlClient):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, nullable=False, comment="任务ID")
    scene_id = db.Column(db.Integer, nullable=False, comment="场景ID")
    result = db.Column(db.SmallInteger, nullable=False, default=STATE[0][0], comment="执行状态")
    more_info = db.Column(db.TEXT, default="{}", comment="任务信息")
    create_time = db.Column(db.DateTime, comment="创建时间", default=datetime.now)

    def __repr__(self):
        return f"Task:{self.task_id}"
