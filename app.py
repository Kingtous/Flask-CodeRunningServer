'''
@Author: Kingtous
@Date: 2020-02-17 23:18:47
@LastEditors: Kingtous
@LastEditTime: 2020-03-02 10:05:04
@Description: Kingtous' Code
'''
from flask import Flask

from app_utils import AppUtils
from router import app_router


def start_server():
    # 猴子补丁，增加并发
    # from gevent import monkey, pywsgi
    #
    # monkey.patch_all()
    # 生成app
    app = Flask(__name__)
    # 初始化APP
    AppUtils.init(app)
    # 配置API
    app_router.set_up_api(app)
    # 配置 pywsgi
    # dapp = DebuggedApplication(app, evalex=True)
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), dapp)
    # server.serve_forever()
    # 运行 flask
    app.run(host="0.0.0.0",
            port=5000,
            debug=True,
            use_reloader=False
            )


if __name__ == '__main__':
    start_server()
