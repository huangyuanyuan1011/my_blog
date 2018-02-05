# 导入类库
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES
from flask_uploads import configure_uploads,patch_request_class


#创建对象
bootstrap = Bootstrap()
db=SQLAlchemy()
mail=Mail()
migrate=Migrate(db=db)
moment = Moment()
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)

# 初始化对象
def config_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app)
    moment.init_app(app)
    #登陆管理初始化
    login_manager.init_app(app)
    #指定登陆的端点
    login_manager.login_view = 'user.login'
    #指定登陆的提示信息
    login_manager.login_message = '需要登陆后才可以访问！'
    #设置session的保护级别：None 用于session保护，basic基本保护，strong高级保护
    login_manager.session_protection = 'strong'

    #上传文件初始化
    configure_uploads(app,photos)
    patch_request_class(app,size=None)
