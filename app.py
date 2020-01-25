from flask import Flask, jsonify
from flask_restful import Api

from api.file_upload import UploadFile, GetFile
from api.test_response import TestResponse
from api.user_login_register import Login, Register, GetToken
from appUtils import AppUtils

# 猴子补丁
# from gevent import monkey
# from gevent import pywsgi
#
# monkey.patch_all()

### 配置
app = Flask(__name__)
# 初始化APP
AppUtils.init(app)
# 配置API
api = Api(app)


@app.route('/')
def hello_world():
    return jsonify()


# TODO 1: 用户登录注册
api.add_resource(Login, '/auth/login')
api.add_resource(Register, '/auth/register')
api.add_resource(GetToken, '/auth/getToken')

# TODO 2: 上传文件
api.add_resource(UploadFile, '/file/upload')
api.add_resource(GetFile, '/uploaded/<file_name>')

# TODO 3: 获取结果
api.add_resource(TestResponse, '/test')

if __name__ == '__main__':
    # from werkzeug.debug import DebuggedApplication
    #
    # dapp = DebuggedApplication(app, evalex=True)
    # server = pywsgi.WSGIServer(('0.0.0.0', 5000), dapp)
    # server.serve_forever()
    app.run(host="0.0.0.0", port=5000, debug=True)
