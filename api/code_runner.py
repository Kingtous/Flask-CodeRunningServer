#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : code_runner.py
# @Author: Kingtous
# @Date  : 2020-01-26
# @Desc  :

# 传入一个url，加入python处理队列，加入成功后返回0

from flask import request, g
from flask_restful import Resource, reqparse

from api.response_code import ResponseClass, ResponseCode
from app.code_manager import CodeBlock
from app_config import auth
from app_utils import AppUtils


class CodeRunnerSubmitAPI(Resource):

    @auth.login_required
    def post(self):
        url = request.json.get("url", None)
        url = AppUtils.get_local_path(url)
        # 先存入CodeResult
        from app.database_models import CodeResult
        code_result = CodeResult()
        code_result.user_id = g.user.id
        code_result.local_path = url
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
                result = session.query(CodeResult).filter_by(user_id=user_id, id=code_id).first()
                if result is None:
                    return ResponseClass.warn(ResponseCode.FILE_NOT_EXIST)
                return ResponseClass.ok_with_data({"status": result.status, "result": result.result})
            except Exception as e:
                print(e)
                return ResponseClass.warn(ResponseCode.SERVER_ERROR)
            finally:
                session.close()
