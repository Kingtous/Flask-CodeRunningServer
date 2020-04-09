'''
@Author: Kingtous
@Date: 2020-02-17 23:18:47
@LastEditors: Kingtous
@LastEditTime: 2020-03-02 10:05:04
@Description: Kingtous' Code
'''
import os

# 导入环境变量
from dotenv import load_dotenv
from flask import Flask, render_template
# 猴子补丁，增加并发
from gevent import pywsgi, monkey
from werkzeug.debug import DebuggedApplication

from app_utils import AppUtils
from router import app_router

dotenv_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path, override=True)  # override=True: 覆写已存在的变量

monkey.patch_all()

# 生成app
app = Flask(__name__)
# 初始化APP
AppUtils.init(app)
# 配置API
app_router.set_up_api(app)


@app.route('/')
def index_page():
    return render_template("index.html")


#
def start_server():
    # 配置 pywsgi
    dapp = DebuggedApplication(app, evalex=True)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), dapp)
    server.serve_forever()
    # 运行 flask
    # app.run(host="0.0.0.0",
    #         port=5000,
    #         debug=True,
    #         use_reloader=False
    #         )


if __name__ == '__main__':
    start_server()
