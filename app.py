from flask import Flask
from flask_restful import Api

from api.code_runner import CodeRunnerSubmitAPI, CodeRunningQueryAPI
from api.file_upload import UploadFile, GetFile
from api.test_response import TestResponse
from api.user_login_register import Login, Register, GetToken
from app_utils import AppUtils

if __name__ == '__main__':
    # 猴子补丁
    # from gevent import monkey
    #
    # monkey.patch_all()

    ### 配置
    app = Flask(__name__)
    # 初始化APP
    AppUtils.init(app)
    # 配置API
    api = Api(app)

    # 1: 用户登录注册
    api.add_resource(Login, '/auth/login')
    api.add_resource(Register, '/auth/register')
    api.add_resource(GetToken, '/auth/getToken')

    # 2: 上传文件
    api.add_resource(UploadFile, '/file/upload')
    api.add_resource(GetFile, '/uploaded/<file_name>')

    # 3: 获取结果
    api.add_resource(TestResponse, '/test')
    api.add_resource(CodeRunnerSubmitAPI, '/code/run')
    api.add_resource(CodeRunningQueryAPI, '/code/getResult')

    # from werkzeug.debug import DebuggedApplication

    # dapp = DebuggedApplication(app, evalex=True)
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), dapp)
    # server.serve_forever()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
