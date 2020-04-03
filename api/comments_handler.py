#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : comments_handler.py
# @Author: Kingtous
# @Date  : 2020-02-03
# @Desc  : 评论
from flask import request, g
from flask_restful import Resource

from api.response_code import ResponseClass, ResponseCode
from app_config import auth
# id = Column(Integer, primary_key=True, autoincrement=True)  # 评论ID
# user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
# code_id = Column(Integer, ForeignKey('Threads.id'), nullable=True)  # 代码ID
# threads_id = Column(Integer, ForeignKey('Code.id'), nullable=False)  # 帖子ID
# content = Column(TEXT)  # 评论内容
# parent_id = Column(Integer, ForeignKey('Comments.id'))
# next_id = Column(Integer, ForeignKey('Comments.id'))
# # datetime.now指的是插入数据的当前时间，datetime.now()指的是建表时间
# create_date = Column(DATETIME, default=datetime.now)
from app_utils import AppUtils


class SubmitComment(Resource):

    @auth.login_required
    def post(self):
        t_id = request.json.get('thread_id', None)  # 帖子ID
        c_id = request.json.get('code_id', None)
        content = request.json.get('content', None)
        if t_id is None or content is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        session = AppUtils.get_session()
        from app.database_models import Threads
        thread = session.query(Threads).filter_by(id=t_id).first()
        if thread is None:
            return ResponseClass.warn(ResponseCode.THREAD_NOT_EXIST)
        from app.database_models import Comments
        new_comment = Comments()
        new_comment.code_id = c_id
        new_comment.user_id = g.user.id
        new_comment.threads_id = t_id
        new_comment.content = content
        result = thread.submit_comment(new_comment)
        if result:
            return ResponseClass.ok()
        else:
            return ResponseClass.warn(ResponseCode.SERVER_ERROR)


class GetComment(Resource):

    @auth.login_required
    def get(self):
        thread_id = request.json.get('thread_id', None)
        session = AppUtils.get_session()
        from app.database_models import Comments
        comments = session.query(Comments).filter_by(threads_id=thread_id).all()
        comments = [item.get_public_dict() for item in comments]
        return ResponseClass.ok_with_data(comments)


class DeleteComment(Resource):

    @auth.login_required
    def post(self):
        thread_id = request.json.get('thread_id', None)
        comment_id = request.json.get('comment_id', None)
        if comment_id is None or thread_id is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        session = AppUtils.get_session()
        from app.database_models import Comments, Threads
        c = session.query(Comments).filter_by(id=comment_id, user_id=g.user.id).first()
        t = session.query(Threads).filter_by(id=thread_id).first()
        if t is None or c is None:
            session.close()
            return ResponseClass.warn(ResponseCode.COMMENT_NOT_FOUND)
        result = t.del_comment(comment_id)
        if result:
            session.close()
            return ResponseClass.ok()
        else:
            session.close()
            return ResponseClass.warn(ResponseCode.SERVER_ERROR)
