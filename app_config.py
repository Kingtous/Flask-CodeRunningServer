import os
from flask_httpauth import HTTPBasicAuth

# 可执行二进制文件配置
from gevent import pool

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
database = None
login_manager = None
SQLBase = None
SQLEngine = None
SQLSessionMaker = None
SQLSession = None
# 协程运行池
running_pool = pool.Pool(10)  # 限制10个协程
code_manager = None
