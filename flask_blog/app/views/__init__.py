from .user import user
from .main import main
from .posts import posts

#蓝本配置

DEFAULT_BLUEPRINT = (
    # （蓝本，url前缀
    (user,""),
    (main,""),
    (posts,"")

 )


# 封装函数完成蓝本注册
def config_blueprint(app):
    for blueprint,url_prefix in DEFAULT_BLUEPRINT:
        app.register_blueprint(blueprint,url_prefix=url_prefix)