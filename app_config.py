import os
from typing import Union

from flask_cache import Cache
from flask_httpauth import HTTPBasicAuth
from flask_mail import Mail
# 可执行二进制文件配置
from flask_sqlalchemy import SQLAlchemy
from gevent import pool
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session

from app.code_manager import CodeManager

PYTHON3_EXE = '/usr/bin/python3'
CPP_EXE = '/usr/bin/g++'
C_EXE = '/usr/bin/gcc'
JAVA_EXE = '/usr/bin/java'
JAVA_COMPILER_EXE = '/usr/bin/javac'
BASH_EXE = '/bin/bash'
# 全局配置
base_url = 'http://127.0.0.1:5000'
base_mysql_connection_url = 'mysql+pymysql://cloud:cloud@localhost:8889/cloud?charset=utf8'
upload_path = os.path.join(os.path.dirname(__file__), 'uploaded')
secret_key = "12345678901234567890123456789012"
# 初始化全局变量
auth = HTTPBasicAuth()  # 可以同时支持token和用户名密码的认证
database: SQLAlchemy = Union[SQLAlchemy]
SQLBase: DeclarativeMeta = Union[DeclarativeMeta]
SQLEngine: Engine = Union[Engine]
SQLSessionMaker: sessionmaker = Union[sessionmaker]
SQLSession: scoped_session = Union[scoped_session]
# 协程运行池
running_pool = pool.Pool(10)  # 限制10个协程
code_manager: CodeManager = Union[CodeManager]
# 邮件系统配置
mail_manager: Mail = Union[None, Mail]
MAIL_SERVER = 'smtp.ym.163.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'robot@kingtous.cn'
MAIL_PASSWORD = 'robot123'
# 缓存
cache: Cache = Union[None, Cache]
