'''
@Author: Kingtous
@Date: 2020-04-20 17:56:23
@LastEditors: Kingtous
@LastEditTime: 2020-04-20 17:56:23
@Description: Kingtous' Code
'''

from flask_restful import Resource, reqparse

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
        session = AppUtils.get_session()
        try:
            items = session.query(Item).filter_by(isOn=True).order_by(Item.name).offset(page * 10).limit(10).all()
            data = []
            for item in items:
                item_dict = AppUtils.serialize(item)
                item_dict.pop('isOn')
                data.append(item_dict)
            return ResponseClass.ok_with_data(data)
        except Exception as e:
            pass
        finally:
            session.close()
