#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : threads_handler.py
# @Author: Kingtous
# @Date  : 2020-01-29
# @Desc  : 帖子API
from flask import request, g
from flask_restful import Resource, reqparse

from api.response_code import ResponseClass, ResponseCode
from app_config import auth
from app_utils import AppUtils


class ThreadsHandler(Resource):
    parser = reqparse.RequestParser()
    page_num_per_request = 10  # 每次返回10篇

    def __init__(self):
        self.parser.add_argument('page')

    # 发布帖子
    @auth.login_required
    def post(self):
        code_id = request.json.get('code_id', None)
        title = request.json.get('title', None)
        subtitile = request.json.get('subtitle', '')
        from app.database_models import Threads
        if not Threads.verify_title(title):
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        thread = Threads()
        thread.user_id = g.user.id
        thread.title = title
        thread.code_id = code_id
        thread.subtitle = subtitile
        AppUtils.add_to_sql(thread).close()
        return ResponseClass.ok()

    @auth.login_required
    # 获取最新帖子，一页10篇
    def get(self):
        args = self.parser.parse_args()
        page_num = int(args.get('page', None))
        if page_num is None or type(page_num) != int or page_num <= 0:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        # 将page_num-1，适应计算
        page_num = page_num - 1
        session = AppUtils.get_session()
        from app.database_models import Threads
        threads = session.query(Threads).offset(page_num * self.page_num_per_request).limit(
            self.page_num_per_request).all()
        threads = [tr.get_public_dict() for tr in threads]
        return ResponseClass.ok_with_data(threads)


# 获取用户自身的帖子
class GetUserThread(Resource):
    parser = reqparse.RequestParser()
    page_num_per_request = 10  # 每次返回10篇

    def __init__(self):
        self.parser.add_argument('page')

    @auth.login_required
    def get(self):
        args = self.parser.parse_args()
        page_num = int(args.get('page', None))
        if page_num is None or type(page_num) != int or page_num <= 0:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        # 将page_num-1，适应计算
        page_num = page_num - 1
        session = AppUtils.get_session()
        from app.database_models import Threads
        threads = session.query(Threads).filter_by(user_id=g.user.id).offset(
            page_num * self.page_num_per_request).limit(
            self.page_num_per_request).all()
        threads = [tr.get_public_dict() for tr in threads]
        return ResponseClass.ok_with_data(threads)


# 删帖
class DeleteThread(Resource):

    @auth.login_required
    def post(self):
        t_id = request.json.get('thread_id', None)
        session = AppUtils.get_session()
        from app.database_models import Threads
        th = session.query(Threads).filter_by(user_id=g.user.id, id=t_id).first()
        if th is None:
            return ResponseClass.warn(ResponseCode.THREAD_NOT_EXIST)
        AppUtils.delete_to_sql(th).close()
        return ResponseClass.ok()
