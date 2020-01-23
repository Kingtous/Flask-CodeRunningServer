import os

from flask import Flask, jsonify, send_from_directory
from flask_restful import Resource, Api, reqparse, abort, request
from werkzeug.utils import secure_filename
from appUtils import AppUtils
# 猴子补丁
from gevent import monkey
from gevent import pywsgi

monkey.patch_all()

### 配置
app = Flask(__name__)
# 初始化APP
AppUtils.init(app)
# 配置API
api = Api(app)
# 新建images文件夹，UPLOAD_PATH就是images的路径
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'uploaded')


@app.route('/')
def hello_world():
    return 'Hello World!'


items = ["bad", "ok", "good", "excellent"]



class TestResponse(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('id', type=int)

    def get(self):
        args = self.parser.parse_args()
        index = args.get('id', None)
        if index is None:
            return jsonify(code=-1, msg="无参数")
        if 0 <= index < len(items):
            return jsonify(code=0, grade=items[index])
        else:
            return jsonify(code=-1, msg="错误的index")

    def post(self):
        index = request.json.get('id', None)
        if index is None:
            return jsonify(code=-1, msg="无参数")
        if 0 <= index < len(items):
            return jsonify(code=0, grade=items[index])
        else:
            return jsonify(code=-1, msg="错误的index")


api.add_resource(UploadFile, '/upload')
api.add_resource(TestResponse, '/grade')
api.add_resource(GetFile, '/uploaded/<file_name>')

if __name__ == '__main__':
    from werkzeug.debug import DebuggedApplication

    dapp = DebuggedApplication(app, evalex=True)
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), dapp)
    server.serve_forever()
    # app.run(port=26785, debug=True)
