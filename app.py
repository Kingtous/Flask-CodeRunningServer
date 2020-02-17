from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.code_runner import CodeRunnerSubmitAPI, CodeRunningQueryAPI
from api.comments_handler import SubmitComment, DeleteComment, GetComment
from api.file_upload import UploadFile, GetFile, GetCodeList
from api.test_response import TestResponse
from api.threads_handler import ThreadsHandler, DeleteThread, GetUserThread
from api.user_login_register import Login, Register, GetToken, UserSignIn, GetCredits
from app_utils import AppUtils

if __name__ == '__main__':
    # 猴子补丁
    from gevent import monkey, pywsgi

    monkey.patch_all()

    ### 配置
    app = Flask(__name__)
    CORS(app)
    # 初始化APP
    AppUtils.init(app)
    # 配置API
    api = Api(app)

    # 1: 用户登录注册
    api.add_resource(Login, '/auth/login')  # 登录
    api.add_resource(Register, '/auth/register')  # 注册
    api.add_resource(GetToken, '/auth/getToken')  # 获取新的token
    api.add_resource(UserSignIn, '/user/signIn')  # 签到
    api.add_resource(GetCredits, '/user/myCredits')  # 查询自己的点数

    # 2: 上传文件
    api.add_resource(UploadFile, '/file/upload')
    api.add_resource(GetFile, '/uploaded/<file_name>')
    api.add_resource(GetCodeList, '/file/getAllCode')

    # 3: 获取结果
    api.add_resource(TestResponse, '/test')
    api.add_resource(CodeRunnerSubmitAPI, '/code/run')
    api.add_resource(CodeRunningQueryAPI, '/code/getResult')

    # 4. 帖子
    api.add_resource(ThreadsHandler, '/threads/push_show')
    api.add_resource(DeleteThread, '/threads/delete')
    api.add_resource(GetUserThread, '/threads/me')
    api.add_resource(SubmitComment, '/threads/comment/submit')
    api.add_resource(DeleteComment, '/threads/comment/del')
    api.add_resource(GetComment, '/threads/comment/get')

    from werkzeug.debug import DebuggedApplication

    dapp = DebuggedApplication(app, evalex=True)
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), dapp)
    server.serve_forever()
    # app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
