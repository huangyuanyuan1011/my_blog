import os

base_dir = os.path.abspath(os.path.dirname(__file__))


# 通用配置
class Config():
    # 密钥
    SECRET_KEY = os.environ.get("SECRET_KEY") or "123456"
    # 数据库操作
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 邮件发送
    MAIL_SERVER = os.environ.get("MAIL_SERVER") or "smtp.163.com"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME") or "15270102382@163.com"
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or "huang1989"
    # bootstrap本地库
    BOOTSTRAP_SERVER_LOCAL = True
    # 长传文件，这是文件默认大小
    MAX_CONTENT_LENGTH = 4 * 1024 * 1024
    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/upload')

    # 初始化函数，完成特定环境的初始化
    @staticmethod
    def init_app(app):
        pass


# 开发环境配置
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-dev.sqlite')


# 测试环境配置
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog-test.sqlite')


# 生产环境配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'blog.sqlite')


# 配置字典
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    # 默认环境
    'default': DevelopmentConfig
}
