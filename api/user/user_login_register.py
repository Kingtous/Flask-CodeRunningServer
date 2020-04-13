# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : user_login_register.py
# @Author: Kingtous
# @Date  : 2020-01-23
# @Desc  : 用户登录注册


import re
from datetime import datetime

from flask import request, jsonify, g
from flask_restful import Resource

import app_utils
from common.constants.response_code import ResponseCode, ResponseClass
from app.database_models import User
from app_config import auth, cache


class Login(Resource):

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        if username is None or password is None:
            return jsonify(code=ResponseCode.FORMAT_ERROR)
        # 查找用户
        session = app_utils.AppUtils.get_session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user is None:
                user = session.query(User).filter_by(mail=username).first()
            if user is None:
                return jsonify(code=ResponseCode.USER_NOT_EXIST)
            if not user.verify_password_only(password):
                return jsonify(code=ResponseCode.PASSWORD_ERROR)
            # 用户验证成功
            return ResponseClass.ok_with_data(
                user.get_self_data()
            )
        finally:
            session.close()


class Register(Resource):

    def post(self):
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        mail = request.json.get('mail', None)
        if username is None or password is None or mail is None or not re.match(
                r'[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+', mail):
            return jsonify(code=ResponseCode.FORMAT_ERROR, msg="用户名密码格式错误")
        session = app_utils.AppUtils.get_session()
        try:
            # 验证用户名
            app_utils.AppUtils.validate_username(username)
            from app.database_models import User
            user = User()
            user.username = username
            user.mail = mail
            user.hash_password(password)
            user.credits = 0
            session.add(user)
            session.commit()
            # 数据库
            from app_config import SQLSession
            return jsonify(code=0, data=user.get_self_data())
        except Exception as e:
            return jsonify(code=-1, msg=e.args[0])
        finally:
            session.close()


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
        try:
            from app.database_models import SignIn
            record = session.query(SignIn).filter_by(user_id=user_id).first()
            from app.database_models import User
            user = session.query(User).filter_by(id=user_id).first()
            if record is None:
                # 从来没签过到
                sign_in_record = SignIn()
                sign_in_record.user_id = user_id
                user.credits = user.credits + 1
                session.add(sign_in_record)
                return ResponseClass.ok()
            else:
                pre_sign_in_time = record.sign_in_time
                current_time = datetime.now()
                if current_time.day > pre_sign_in_time.day:
                    # 可以签到，更新时间
                    record.sign_in_time = current_time
                    user.credits = user.credits + 1
                    return ResponseClass.ok()
                else:
                    return ResponseClass.warn(ResponseCode.ALREADY_SIGN_IN)
        finally:
            session.commit()
            session.close()


class UserResetPassword(Resource):

    def post(self):
        code = request.json.get('code', None)
        new_password = request.json.get('new_password', None)
        if code is None or new_password is None or not User.password_illigal(new_password):
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        else:
            user_id = cache.get(code)
            if user_id is None:
                return ResponseClass.warn(ResponseCode.SERVER_FORBIDDEN)
            session = app_utils.AppUtils.get_session()
            try:
                user = session.query(User).filter_by(id=user_id).first()
                if user is None:
                    return ResponseClass.warn(ResponseCode.USER_NOT_EXIST)
                user.hash_password(new_password)
                session.commit()
                cache.delete(code)
                cache.delete(user_id)
                return ResponseClass.ok_with_data(user.get_self_data())
            finally:
                session.close()
