#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : response_code.py
# @Author: Kingtous
# @Date  : 2020-01-25
# @Desc  : 存储响应的Code类型
from flask import jsonify


class ResponseCode:
    # 正常返回
    THREAD_NOT_EXIST = 1007  # 帖子不存在
    USER_ALREADY_EXIST = 1004  # 用户名不可用
    OK_RESPONSE = 0  # 正常返回
    # 不正常的返回值
    LOGIN_REQUIRED = 1000  # 需要登录/token过期
    USER_NOT_EXIST = 1001  # 用户名不存在
    FORMAT_ERROR = 1002  # 格式错误
    PASSWORD_ERROR = 1003  # 密码错误
    SUBMIT_ERROR = 1004  # 提交错误
    FILE_NOT_EXIST = 1005  # 文件不存在
    SERVER_ERROR = 1006  # 服务器故障


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
