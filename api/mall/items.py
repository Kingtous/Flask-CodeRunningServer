'''
@Author: Kingtous
@Date: 2020-04-20 17:56:23
@LastEditors: Kingtous
@LastEditTime: 2020-04-20 17:56:23
@Description: Kingtous' Code
'''
from flask import request, g
from flask_restful import Resource, reqparse
from sqlalchemy import desc

import app_config as conf
from app.database_models import Item
from app_utils import AppUtils
from common.constants.response_code import ResponseClass, ResponseCode


# 获取兑换的物品
class GetItems(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument("page", int)

    @conf.auth.login_required
    def get(self):
        args = self.parser.parse_args()
        page = args.get('page', None)
        if page is None:
            return ResponseClass.warn(ResponseCode.FORMAT_ERROR)
        if g.user.role == conf.USER_ROLE_ADMIN:
            session = AppUtils.get_session()
            try:
                items = session.query(Item).order_by(desc(Item.id)).offset(page * 10).limit(10).all()
                data = []
                for item in items:
                    item_dict = AppUtils.serialize(item)
                    data.append(item_dict)
                return ResponseClass.ok_with_data(data)
            except Exception as e:
                pass
            finally:
                session.close()
        else:
            session = AppUtils.get_session()
            try:
                items = session.query(Item).filter_by(isOn=True).order_by(Item.name).offset(page * 10).limit(10).all()
                data = []
                for item in items:
                    item_dict = AppUtils.serialize(item)
                    data.append(item_dict)
                return ResponseClass.ok_with_data(data)
            except Exception as e:
                pass
            finally:
                session.close()


# 添加/修改Items
# 传入id表示修改
class AddItems(Resource):

    @conf.auth.login_required
    def post(self):
        if g.user.role == conf.USER_ROLE_USER:
            return ResponseClass.warn(ResponseCode.NOT_ROOT)
        else:
            session = AppUtils.get_session()
            id = request.json.get('id', None)
            print(id)
            item: Item
            if id is not None:
                # 修改items
                item = session.query(Item).filter_by(id=id).first()
            else:
                item = Item()
            item.name = request.json.get('name')
            item.detail = request.json.get('detail')
            item.credits = request.json.get('credits')
            item.isOn = request.json.get('isOn')
            item.img = request.json.get('img')
            if id is None:
                session.add(item)
            try:
                session.commit()
                return ResponseClass.ok_with_data({"id": item.id})
            finally:
                session.close()


# 更改物品状态
class ChangeItemStatus(Resource):

    @conf.auth.login_required
    def post(self):
        if g.user.role == conf.USER_ROLE_USER:
            return ResponseClass.warn(ResponseCode.NOT_ROOT)
        else:
            session = AppUtils.get_session()
            try:
                item = session.query(Item).filter_by(id=request.json.get("id")).first()
                if item is not None:
                    item.isOn = not item.isOn
                    session.commit()
                    return ResponseClass.ok_with_data(item.isOn)
                else:
                    return ResponseClass.warn(ResponseCode.ITEM_NOT_FOUND)
            finally:
                session.close()
