#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : test_response.py
# @Author: Kingtous
# @Date  : 2020-01-23
# @Desc  : 测试用接口
from flask import jsonify, request
from flask_restful import Resource, reqparse

from app_config import auth

items = ["bad", "ok", "good", "excellent"]


class TestResponse(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument('id', type=int)

    @auth.login_required
    def get(self):
        # params
        args = self.parser.parse_args()
        index = args.get('id', None)
        if index is None:
            return jsonify(code=-1, msg="无参数id,id可为0,1,2,3")
        if 0 <= index < len(items):
            return jsonify(code=0, grade=items[index])
        else:
            return jsonify(code=-1, msg="错误的index")

    def post(self):
        try:
            # form
            index = request.json.get('id', None)
            if index is None:
                return jsonify(code=-1, msg="无参数")
            if 0 <= index < len(items):
                return jsonify(code=0, grade=items[index])
            else:
                return jsonify(code=-1, msg="错误的index")
        except AttributeError as e:
            return jsonify(code=-1, msg="请传递json数据")
