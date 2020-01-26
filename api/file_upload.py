import datetime
import os

from flask import jsonify, send_from_directory, g, request
from flask_restful import Resource
from werkzeug.utils import secure_filename

import app_config as Cf
from api.response_code import ResponseCode
from app_utils import AppUtils


class UploadFile(Resource):

    @Cf.auth.login_required
    def post(self):
        file = request.files.get('file', None)
        if not file:
            return jsonify(code=-1, msg="参数不对")
        filename = secure_filename(
            g.user.username + datetime.datetime.now().strftime('_%H-%M-%S-%f_') + file.filename).lower()
        file.save(os.path.join(Cf.upload_path, filename))
        return jsonify(code=ResponseCode.OK_RESPONSE,
                       data={'url': AppUtils.get_network_url(os.path.join(Cf.upload_path, filename))})


class GetFile(Resource):

    @Cf.auth.login_required
    def get(self, file_name):
        return send_from_directory(Cf.upload_path, file_name)
