import sys

from qiniu import Auth

from common.constants.tokens import QINIU_SECRET_KEY, QINIU_ACCESS_KEY, BUCKET_NAME


def get_upload_token() -> str:
    try:
        q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
        token = q.upload_token(BUCKET_NAME)
        return token
    except Exception as e:
        sys.stderr.write(e)
        return ""
