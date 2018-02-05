from app.extensions import db
from datetime import datetime


class Posts(db.Model):
    __tablename__="posts"
    id = db.Column(db.Integer,primary_key=True)
    rid = db.Column(db.Integer,default=0,index=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime,default=datetime.utcnow)
    #添加外键 表名.字段名

    uid = db.Column(db.Integer,db.ForeignKey('users.id'))