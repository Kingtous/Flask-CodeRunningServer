import os

class AppBaseConfig:
    base_url = 'http://127.0.0.1:5000'
    base_mysql_connection_url = 'mysql+pymysql://cloud:cloud@localhost:8889/cloud?charset=utf8'
    UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'uploaded')
    database = None
