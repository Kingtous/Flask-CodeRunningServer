import os
from flask_sqlalchemy import  SQLAlchemy
import appConfig as config


class AppUtils:

    @staticmethod
    def init(app):
        # 初始化数据库
        app.config['SQLALCHEMY_DATABASE_URI'] = config.AppBaseConfig.base_mysql_connection_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
        app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
        config.AppBaseConfig.database = SQLAlchemy(app)
        import database
        config.AppBaseConfig.database.create_all()


    @staticmethod
    def get_network_url(local_url):
        return local_url.replace(os.path.dirname(__file__), config.AppBaseConfig.base_url)
