#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

# @File  : code_runner.py
# @Author: Kingtous
# @Date  : 2020-01-26
# @Desc  :

# 传入一个url，加入python处理队列，加入成功后返回0

from flask import request, g
from flask_restful import Resource, reqparse

from app.code_manager import CodeBlock
from app_config import auth
from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode


class CodeRunnerSubmitAPI(Resource):

    @auth.login_required
    def post(self):
        url = request.json.get("url", None)
        url = AppUtils.get_local_path(url)

        session = AppUtils.get_session()
        from app.database_models import Code
        code = session.query(Code).filter_by(local_path=url).first()
        if code is None:
            return ResponseClass.warn(ResponseCode.FILE_NOT_EXIST)
        session.close()
        # 先存入CodeResult
        from app.database_models import CodeResult
        code_result = CodeResult()
        code_result.code_id = code.id
        code_result.user_id = g.user.id
        from app_config import code_manager
        session = AppUtils.add_to_sql(code_result)
        block = CodeBlock(user_id=code_result.user_id, task_id=code_result.id)
        session.close()
        return_value = code_manager.add_task(block)
        if return_value:
            return ResponseClass.ok_with_data({"code_id": code_result.id})
        else:
            return ResponseClass.warn(ResponseCode.SUBMIT_ERROR)


class CodeRunningQueryAPI(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('code_id', type=int)

    @auth.login_required
    def get(self):
        user_id = g.user.id
        args = self.parser.parse_args()
        code_id = args.get('code_id', None)
        if code_id is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        else:
            from app_config import SQLSession
            session = SQLSession()
            try:
                from app.database_models import CodeResult
                result = session.query(CodeResult).filter_by(user_id=user_id, code_id=code_id).first()
                if result is None:
                    return ResponseClass.warn(ResponseCode.FILE_NOT_EXIST)
                return ResponseClass.ok_with_data({"status": result.status, "result": result.result})
            except Exception as e:
                print(e)
                return ResponseClass.warn(ResponseCode.SERVER_ERROR)
            finally:
                session.close()
