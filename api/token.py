from flask_restful import Resource

from api.response_code import ResponseClass, ResponseCode
from app_config import auth
from common.utils.qiniu_util import get_upload_token


class UploadTokenAPI(Resource):

    @auth.login_required
    def get(self):
        token = get_upload_token()
        if token == "":
            return ResponseClass.warn(ResponseCode.SERVER_ERROR)
        else:
            return ResponseClass.ok_with_data(get_upload_token())
