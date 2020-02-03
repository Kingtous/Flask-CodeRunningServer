#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : user_login_register.py
# @Author: Kingtous
# @Date  : 2020-01-23
# @Desc  : 用户登录注册


# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : user_login_register.py
# @Author: Kingtous
# @Date  : 2020-01-24
# @Desc  :
from datetime import datetime

from flask import request, jsonify, g
from flask_restful import Resource
from wtforms import ValidationError

import app_utils
from api.response_code import ResponseCode, ResponseClass
from app_config import auth


class Login(Resource):

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if username is None or password is None:
            return jsonify(code=ResponseCode.FORMAT_ERROR)
        # 查找用户
        from app.database_models import User
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify(code=ResponseCode.USER_NOT_EXIST)
        if not user.verify_password_only(password):
            return jsonify(code=ResponseCode.PASSWORD_ERROR)
        # 用户验证成功
        token = user.generate_auth_token()
        return jsonify(code=ResponseCode.OK_RESPONSE, data={
            "token": token,
            "username": username
        })


class Register(Resource):

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if username is None or password is None:
            return jsonify(code=ResponseCode.FORMAT_ERROR, msg="用户名密码格式错误")
        try:
            # 验证用户名
            app_utils.AppUtils.validate_username(username)
            from app.database_models import User
            user = User()
            user.username = username
            user.hash_password(password)
            # 数据库
            from app_config import SQLSession
            app_utils.AppUtils.add_to_sql(user)
            token = user.generate_auth_token()
            return jsonify(code=0, data={"username": username, "token": token, "credits": user.credits})
        except ValidationError as e:
            return jsonify(code=-1, msg=e.args[0])


class GetToken(Resource):

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return ResponseClass.ok_with_data({'token': token})


class GetCredits(Resource):

    @auth.login_required
    def get(self):
        return ResponseClass.ok_with_data({'credits': g.user.credits})


class UserSignIn(Resource):

    @auth.login_required
    def post(self):
        user_id = g.user.id
        session = app_utils.AppUtils.get_session()
        from app.database_models import SignIn
        record = session.query(SignIn).filter_by(user_id=user_id).first()
        from app.database_models import User
        user = session.query(User).filter_by(id=user_id).first()
        if record is None:
            # 从来没签过到
            sign_in_record = SignIn()
            sign_in_record.user_id = user_id
            user.credits = user.credits + 1
            app_utils.AppUtils.add_to_sql(sign_in_record)
            app_utils.AppUtils.close_sql(session)
            return ResponseClass.ok()
        else:
            pre_sign_in_time = record.sign_in_time
            current_time = datetime.now()
            if current_time.day > pre_sign_in_time.day:
                # 可以签到，更新时间
                record.sign_in_time = current_time
                user.credits = user.credits + 1
                app_utils.AppUtils.update_sql(session)
                app_utils.AppUtils.close_sql(session)
                return ResponseClass.ok()
            else:
                app_utils.AppUtils.close_sql(session)
                return ResponseClass.warn(ResponseCode.ALREADY_SIGN_IN)
