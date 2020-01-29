from datetime import datetime

from flask import g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.mysql import *

import app_config as Cf
# db
from app.code_manager import CodeStatus

db = Cf.database
auth = HTTPBasicAuth()


# 用户表
class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(128))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password_only(self, password):
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    @Cf.auth.verify_password
    def verify_password(username_or_token, password):
        # first try to authenticate by token
        user = User.verify_auth_token(username_or_token)
        if not user:
            # try to authenticate with username/password
            user = User.query.filter_by(username=username_or_token).first()
            if not user or not user.verify_password_only(password):
                return False
        g.user = user
        return True

    def generate_auth_token(self, expiration=3600):
        s = Serializer(Cf.secret_key, expires_in=expiration)
        return s.dumps({'id': self.id, 'username': self.username}).decode()

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(Cf.secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


# 积分表
class Points(db.Model):
    __tablename__ = 'Points'
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), primary_key=True)  # 用户ID
    points = Column(Integer)  # 积分数


# 代码保存
class Code(db.Model):
    __tablename__ = 'Code'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 代码的ID
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)
    code_type = Column(Integer, nullable=True)
    local_path = Column(String(256), nullable=False)  # 本地路径
    create_date = Column(DATETIME, default=datetime.now)

    # 转换为下载地址
    def get_download_url(self):
        from app_utils import AppUtils
        return AppUtils.get_network_url(self.local_path)

    def get_public_dict(self):
        d = dict()
        d['id'] = self.id
        d['code_type'] = self.code_type
        d['local_path'] = self.get_download_url()
        d['create_date'] = self.create_date.timestamp()
        return d


# 代码执行结果
class CodeResult(db.Model):
    __tablename__ = 'CodeResult'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 代码执行结果id
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)
    code_id = Column(Integer, ForeignKey('Code.id', ondelete="CASCADE"), nullable=False)  # 本地路径
    status = Column(Integer, default=CodeStatus.waiting)  # 代码执行状态
    result = Column(MEDIUMTEXT, default="")  # MediumBlob最大支持16MB文件，LongBlob最大支持4GB


# 帖子表
class Threads(db.Model):
    __tablename__ = 'Threads'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 帖子ID
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)  # 发帖人的ID
    code_id = Column(Integer, ForeignKey('Code.id'), nullable=True)  # 代码ID
    title = Column(TINYTEXT)  # 帖子标题
    subtitle = Column(TEXT)  # 副标题，可能作为正文内容

    @staticmethod
    def verify_title(title):
        if title is None or type(title) != str or title.strip() == '':
            return False
        return True

    def get_public_dict(self):
        d = dict()
        d['id'] = self.id
        d['title'] = self.title
        d['subtitle'] = self.subtitle
        from app_utils import AppUtils
        session = AppUtils.get_session()
        code = session.query(Code).filter_by(id=self.code_id).first()
        if code is not None:
            d['code_url'] = code.get_download_url()
        else:
            d['code_url'] = ''
        d['user_id'] = self.user_id
        d['username'] = session.query(User).filter_by(id=self.user_id).first().username
        session.close()
        return d


# 评论表
class Comments(db.Model):
    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 评论ID
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    code_id = Column(Integer, ForeignKey('Threads.id'), nullable=True)  # 代码ID
    threads_id = Column(Integer, ForeignKey('Code.id'), nullable=False)  # 帖子ID
    content = Column(TEXT)  # 评论内容
    parent_id = Column(Integer, ForeignKey('Comments.id'))
    next_id = Column(Integer, ForeignKey('Comments.id'))
    # datetime.now指的是插入数据的当前时间，datetime.now()指的是建表时间
    create_date = Column(DATETIME, default=datetime.now)


# 代码分享表
class CodeSharing(db.Model):
    __tablename__ = 'CodeSharing'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 分享的ID
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)  # 分享人
    code_id = Column(Integer, ForeignKey('Code.id', ondelete="CASCADE"), nullable=False)  # 本地路径
    like_nums = Column(Integer, default=0)  # 喜欢数
    dislike_nums = Column(Integer, default=0)  # 不喜欢数
    is_private = Column(BOOLEAN, default=True)  # 是否为私有
