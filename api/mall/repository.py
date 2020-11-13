#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : repository.py
# @Author: Kingtous
# @Date  : 2020/4/20
# @Desc  :

from flask import g
from flask_restful import Resource, reqparse

import app_config as conf
from app.database_models import Repository
from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode


# 获取兑换的物品
class GetRepositoryItems(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument("page", int)

    @conf.auth.login_required
    def get(self):
        args = self.parser.parse_args()
        page = args.get('page', None)
        if page is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        session = AppUtils.get_session()
        try:
            repository_items = session.query(Repository).filter_by(user_id=g.user.id).order_by(
                conf.database.desc(Repository.create_date)).offset(
                page * 10).limit(
                10).all()
            data = []
            for repository_item in repository_items:
                item_data = AppUtils.serialize(repository_item.item)
                item_data['repo_id'] = repository_item.id
                data.append(item_data)
            return ResponseClass.ok_with_data(data)
        except Exception as e:
            pass
        finally:
            session.close()
