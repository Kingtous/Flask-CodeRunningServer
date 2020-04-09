import os
import re
import shutil
import sys

import pyfiglet
from flask import jsonify
from flask_cache import Cache
from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from wtforms import ValidationError

import app_config as Cf
from api.response_code import ResponseCode
from app.code_manager import CodeManager


# 全局Utils
class AppUtils:

    @staticmethod
    def init(flask_app):
        # 增加CORS跨域支持
        CORS(flask_app)
        # APP Server Banner
        print(pyfiglet.figlet_format("Kingtous Kits"))
        print("Code Running Server By Kingtous")
        # 初始化secret_key
        flask_app.config['SECRET_KEY'] = Cf.secret_key
        # 防范CSRF攻击
        flask_app.config["CSRF_ENABLED"] = True
        # 初始化数据库
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = Cf.base_mysql_connection_url
        flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        flask_app.config["SQLALCHEMY_ECHO"] = False
        db = SQLAlchemy(flask_app)
        Cf.database = db
        Cf.SQLBase = declarative_base()
        Cf.SQLEngine = create_engine(Cf.base_mysql_connection_url,
                                     pool_recycle=7200,
                                     pool_size=100,
                                     echo=False)
        Cf.SQLSessionMaker = sessionmaker(bind=Cf.SQLEngine)
        Cf.SQLSession = scoped_session(Cf.SQLSessionMaker)  # scoped_session保证线程安全
        # 初始化邮件系统
        AppUtils.init_mail(flask_app)
        # 必须import database_models初始化数据库各类!
        import app.database_models
        print(app.database_models)
        try:
            Cf.database.create_all()
        except Exception as e:
            sys.stderr.write('Database Connect Error: %s\n' % e.args[0])
            exit(0)

        # 未登录回调
        @Cf.auth.error_handler
        def unauthorized():
            return jsonify(code=ResponseCode.LOGIN_REQUIRED)

        # 启动代码运行服务
        Cf.code_manager = CodeManager()
        # 启动缓存
        # TODO simple只是用dict保存，后期使用redis替换
        Cf.cache = Cache(flask_app, config={'CACHE_TYPE': 'simple'})
        # 初始化完成，回调
        AppUtils.on_init_success(flask_app)

    # 初始化成功
    @staticmethod
    def on_init_success(flask_app):
        with flask_app.app_context():
            # message = Message(subject='Code Running Server服务变更',
            #                   recipients=['kingtous@qq.com'],
            #                   body='服务已启动通知')
            # Cf.mail_manager.send(message)
            # print("已发送测试邮件")
            pass

    @staticmethod
    def init_mail(app):
        app.config['MAIL_SERVER'] = Cf.MAIL_SERVER
        app.config['MAIL_PORT'] = Cf.MAIL_PORT
        app.config['MAIL_USE_TLS'] = Cf.MAIL_USE_TLS
        app.config['MAIL_USERNAME'] = Cf.MAIL_USERNAME
        app.config['MAIL_PASSWORD'] = Cf.MAIL_PASSWORD
        app.config['MAIL_USE_SSL'] = Cf.MAIL_USE_SSL
        app.config['MAIL_DEFAULT_SENDER'] = Cf.MAIL_USERNAME
        Cf.mail_manager = Mail(app)

    @staticmethod
    def get_network_url(local_url):
        return local_url.replace(os.path.dirname(__file__), Cf.base_url)

    @staticmethod
    def get_local_path(network_url):
        return network_url.replace(Cf.base_url, os.path.dirname(__file__))

    @staticmethod
    def validate_username(username):
        from app.database_models import User
        session = AppUtils.get_session()
        user = session.query(User).filter_by(username=username).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    @staticmethod
    def get_session() -> Session:
        return Cf.SQLSession()

    @staticmethod
    def delete_to_sql(data) -> Session:
        session = Cf.SQLSession()
        session.delete(data)
        session.commit()
        return session

    @staticmethod
    def add_to_sql(data) -> Session:
        session = Cf.SQLSession()
        session.add(data)
        session.commit()
        return session

    @staticmethod
    def update_sql(session):
        session.commit()

    @staticmethod
    def close_sql(session):
        session.close()

    @staticmethod
    def copy_file(src, dst):
        try:
            shutil.copyfile(src, dst)
            return dst
        except IOError:
            return None

    @staticmethod
    def get_java_class_name(path):
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            try:
                file_name = re.search('^[\s]*public[\s]+class[\s]+[a-z|A-z]+', f.read()).group()
                if file_name is None:
                    return None
                class_name = re.split('\s+', file_name)[-1]
                return class_name
            except Exception as e:
                print(e)
                return None
