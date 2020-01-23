

class UploadFile(Resource):
    def post(self):
        file = request.files.get('file', None)
        if not file:
            return jsonify(code=-1, msg="参数不对")
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_PATH, filename))
        return jsonify(code=0, url=AppUtils.get_network_url(os.path.join(UPLOAD_PATH, filename)))


class GetFile(Resource):
    def get(self, file_name):
        return send_from_directory(UPLOAD_PATH, file_name)

