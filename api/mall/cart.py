#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cart.py
# @Author: Kingtous
# @Date  : 2020/4/20
# @Desc  : 购物车：添加


'''
@Author: Kingtous
@Date: 2020-04-20 17:56:23
@LastEditors: Kingtous
@LastEditTime: 2020-04-20 17:56:23
@Description: Kingtous' Code
'''
from flask import g, request
from flask_restful import Resource, reqparse

import app_config as conf
from app.database_models import Cart, Repository, User
from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode


# 获取兑换的物品
class GetCart(Resource):
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
            cart_items = session.query(Cart).filter_by(user_id=g.user.id).order_by(
                conf.database.desc(Cart.create_date)).offset(
                page * 10).limit(
                10).all()
            data = []
            for cart_item in cart_items:
                item_data = AppUtils.serialize(cart_item.item)
                item_data['cart_item_id'] = cart_item.id
                data.append(item_data)
            return ResponseClass.ok_with_data(data)
        except Exception as e:
            pass
        finally:
            session.close()


class AddCart(Resource):

    @conf.auth.login_required
    def post(self):
        cart_id = int(request.json.get("item_id", None))
        if cart_id is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        session = AppUtils.get_session()
        try:
            cart = Cart()
            cart.item_id = cart_id
            cart.user_id = g.user.id
            session.add(cart)
            session.commit()
            return ResponseClass.ok()
        except Exception as e:
            pass
        finally:
            session.close()


class DelCart(Resource):

    @conf.auth.login_required
    def post(self):
        cart_id = int(request.json.get("item_id", None))
        if cart_id is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        session = AppUtils.get_session()
        try:
            item = session.query(Cart).filter_by(user_id=g.user.id, id=cart_id).first()
            if item is None:
                return ResponseClass.warn(ResponseCode.ITEM_NOT_FOUND)
            session.delete(item)
            session.commit()
            return ResponseClass.ok()
        except Exception as e:
            pass
        finally:
            session.close()


class BuyCarts(Resource):

    @conf.auth.login_required
    def post(self):
        ids = request.json.get("ids", [])
        if len(ids) == 0:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        session = AppUtils.get_session()
        total_credits = g.user.credits
        try:
            need_paid = 0
            cart_item = []
            for id in ids:
                item = session.query(Cart).filter_by(id=id).first()
                if item is not None:
                    need_paid += item.item.credits
                    cart_item.append(item)
            if need_paid > total_credits:
                return ResponseClass.warn(ResponseCode.NO_ENOUGH_CREDITS)
            else:
                # cart_id -> repository
                user = session.query(User).filter_by(id=g.user.id).first()
                user.credits -= need_paid
                for cart in cart_item:
                    repo = Repository()
                    repo.user_id = g.user.id
                    repo.item_id = cart.item_id
                    session.add(repo)
                    session.delete(cart)
                session.commit()
                return ResponseClass.ok_with_data(user.credits)
        except Exception as e:
            pass
        finally:
            session.close()
