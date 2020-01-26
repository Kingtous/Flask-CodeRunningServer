#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : response_code.py
# @Author: Kingtous
# @Date  : 2020-01-25
# @Desc  : 存储响应的Code类型

class ResponseCode:
    # 正常返回
    USER_ALREADY_EXIST = 1004
    OK_RESPONSE = 0
    # 不正常的返回值
    LOGIN_REQUIRED = 1000
    USER_NOT_EXIST = 1001
    FORMAT_ERROR = 1002
    PASSWORD_ERROR = 1003
