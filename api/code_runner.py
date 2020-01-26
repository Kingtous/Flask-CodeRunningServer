#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : code_runner.py
# @Author: Kingtous
# @Date  : 2020-01-26
# @Desc  :

# 传入一个url，加入python处理队列，加入成功后返回0

from flask import request, g
from flask_restful import Resource

from api.response_code import ResponseClass, ResponseCode
from app.code_manager import CodeBlock
from app_config import auth
from app_utils import AppUtils


class CodeRunnerAPI(Resource):

    @auth.login_required
    def get(self):
        url = request.json.get("url", None)
        url = AppUtils.get_local_path(url)
        # 先存入CodeResult
        from database_models import CodeResult
        code_result = CodeResult()
        code_result.user_id = g.user.id
        code_result.local_path = url
        from app_config import code_manager
        session = AppUtils.add_to_sql(code_result)
        block = CodeBlock(user_id=code_result.user_id, task_id=code_result.id)
        session.close()
        return_value = code_manager.add_task(block)
        if return_value:
            return ResponseClass.ok()
        else:
            return ResponseClass.warn(ResponseCode.SUBMIT_ERROR)
