from app.extensions import db
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app,flash
from flask_login import UserMixin
from app.extensions import login_manager
from app.models.posts import Posts

class User(db.Model,UserMixin):
    __tablename__="users"
    id = db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(32),unique=True)
    password_hash=db.Column(db.String(128))
    email=db.Column(db.String(64),unique=True)
    confirm =db.Column(db.Boolean,default=False)
    icon = db.Column(db.String(64),default="default.jpg")
    #在关联模型中添加反向引用
    # 参数1：关联的模型
    # backref：反向引用字段名
    # lazy：加载时机，dynamic不加载数据，但是提供数据的查询
    # 一对一关系添加：uselist = False
    posts = db.relationship('Posts',backref='user',lazy="dynamic")
    #添加收藏功能
    favorites = db.relationship('Posts',secondary="collections",
                                backref=db.backref("users", lazy="dynamic"), lazy="dynamic")
    # 保护密码属性
    @property
    def password(self):
        raise AttributeError('密码是不可读属性')
    # 设置密码时，保存加密后的hash值
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 密码校验，正确返回True，错误返回False
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成账户激活的token
    def generate_activate_token(self, expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id})

    # 校验账户激活的token
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        u = User.query.get(data.get('id'))
        if not u:
            # flash('用户不存在')
            return False
        if not u.confirm:  # 账户没有激活
            u.confirm = True
            db.session.add(u)
        return True

    #判断该用户是否收藏了指定的博客

    def is_favorite(self,pid):
        #获取所有收藏博客
        favorites = self.favorites.all()
        posts=list(filter(lambda p: p.id==pid ,favorites))
        if len(posts)>0:
            return True
        return False
    #添加收藏
    def add_favorite(self,pid):
        p = Posts.query.get(pid)
        self.favorites.append(p)

    # 取消收藏
    def del_favorite(self,pid):
        p = Posts.query.get(pid)
        self.favorites.remove(p)
#登陆认证的回掉函数
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))