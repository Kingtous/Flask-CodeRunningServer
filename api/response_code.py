#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : response_code.py
# @Author: Kingtous
# @Date  : 2020-01-25
# @Desc  : 存储响应的Code类型
from flask import jsonify


class ResponseCode:
    # 正常返回
    USER_ALREADY_EXIST = 1004
    OK_RESPONSE = 0
    # 不正常的返回值
    LOGIN_REQUIRED = 1000
    USER_NOT_EXIST = 1001
    FORMAT_ERROR = 1002
    PASSWORD_ERROR = 1003
    SUBMIT_ERROR = 1004


class ResponseClass:

    @staticmethod
    def ok():
        return jsonify(code=ResponseCode.OK_RESPONSE)

    @staticmethod
    def ok_with_data(data):
        return jsonify(code=ResponseCode.OK_RESPONSE, data=data)

    @staticmethod
    def warn(code_int):
        return jsonify(code=code_int)
