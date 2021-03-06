'''
@Author: Kingtous
@Date: 2020-01-29 12:51:22
@LastEditors: Kingtous
@LastEditTime: 2020-03-02 10:06:16
@Description: Kingtous' Code
'''
#  Copyright (C) <2020> Kingtous
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
#  documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
#   rights to use,copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
#   and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#  　　
#  The above copyright notice and this permission notice shall be included in all copies or
#  substantial portions of the Software.
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
#  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
#  LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
#  TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.

import datetime
import os

from flask import jsonify, send_from_directory, g, request, make_response
from flask_restful import Resource
from werkzeug.utils import secure_filename

import app_config as Cf
from common.constants.response_code import ResponseCode, ResponseClass
from app.database_models import Code
from app_utils import AppUtils


class UploadFile(Resource):

    @Cf.auth.login_required
    def post(self):
        content = request.json.get('content', None)
        file_name = request.json.get('fileName', None)
        if not content or not file_name:
            return jsonify(code=-1, msg="参数不对")
        filename = secure_filename(
            g.user.username + datetime.datetime.now().strftime('_%H-%M-%S-%f_') + file_name).lower()
        local_path = os.path.join(Cf.upload_path, filename)
        # file.save(local_path)
        file = open(local_path, encoding="utf-8", mode="w")
        file.write(content)
        file.close()
        # 写入数据库
        from app.database_models import Code
        code = Code()
        code.user_id = g.user.id
        code.local_path = local_path
        # 根据后缀判断语言
        suffix = os.path.splitext(filename)[-1]
        from app.code_manager import CodeType
        if suffix == '.py':
            code.code_type = CodeType.PYTHON3
        elif suffix == '.c':
            code.code_type = CodeType.C
        elif suffix == '.cpp':
            code.code_type = CodeType.CPP
        elif suffix == '.java':
            code.code_type = CodeType.JAVA
        else:
            code.code_type = CodeType.FILE
        session = AppUtils.get_session()
        try:
            session.add(code)
            session.commit()
            return jsonify(code=ResponseCode.OK_RESPONSE,
                           data={'id': code.id,
                                 'url': AppUtils.get_network_url(os.path.join(Cf.upload_path, filename))})
        finally:
            session.close()


class DelFile(Resource):

    @Cf.auth.login_required
    def get(self, id):
        session = AppUtils.get_session()
        try:
            from app.database_models import Code
            code = session.query(Code).filter_by(user_id=g.user.id, id=id).first()
            if code is not None:
                session.delete(code)
            return jsonify(ResponseClass.ok())
        finally:
            session.close()


class GetFile(Resource):

    def get(self, file_name):
        args = request.args
        print(args)
        token = args.get('token', None)
        if token is None:
            return ResponseClass.warn(-2)
        from app.database_models import User
        user = User.verify_auth_token(token)
        if user is not None:
            response = make_response(send_from_directory(Cf.upload_path, file_name, as_attachment=True))
            response.headers["Content-Type"] = "application/octet-stream"
            response.headers["Accept-ranges"] = "bytes"
            response.headers["Content-Disposition"] = "attachment; filename={}".format(
                file_name.encode().decode('latin-1'))
            return response
        else:
            return ResponseClass.warn(-1)


class GetCodeList(Resource):
    @Cf.auth.login_required
    def get(self, offset: int):
        session = AppUtils.get_session()
        try:
            result = Code.get_code(session, g.user.id, offset)
            result = list(map(Code.get_public_dict, result))
            return ResponseClass.ok_with_data(result)
        finally:
            session.close()
