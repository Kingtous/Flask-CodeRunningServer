from datetime import datetime
from typing import List

from flask import g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.dialects.mysql import *
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql.sqltypes import Boolean

import app_config as Cf
from app.code_manager import CodeStatus
from app_utils import AppUtils
# db
from common.constants.response_code import ResponseClass, ResponseCode

db = Cf.database
auth = HTTPBasicAuth()

expiration = 3600
s = Serializer(Cf.secret_key, expires_in=expiration)


# 用户表
class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    nickname = db.Column(db.String(50), default="Fresh Coder")
    mail = db.Column(db.String(128), unique=True, nullable=False, index=True)
    avatar_url = db.Column(db.String(255),
                           default="http://hbimg.b0.upaiyun.com/5ecab4b5752dea92f62f472cdea1a387f806b43a85b7-4O5QSj_fw236")
    password_hash = db.Column(db.String(128))
    credits = Column(Integer, default=0)  # 积分
    likes = Column(Integer, default=0)  # 点赞数
    # TODO 职责
    role = Column(Integer, default=Cf.USER_ROLE_USER)  # 职责

    @staticmethod
    def password_illigal(password):
        # TODO
        return True

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password_only(self, password):
        return pwd_context.verify(password, self.password_hash)

    def get_self_data(self):
        return {"id": self.id, "username": self.username, "token": self.generate_auth_token(), "credits": self.credits,
                "avatar_url": self.avatar_url, "nickname": self.nickname, "role": self.role}

    # 用于其他访问的数据
    def get_minimal_data(self):
        return {"id": self.id, "username": self.username, "avatar_url": self.avatar_url, "nickname": self.nickname,
                "role": self.role}

    @staticmethod
    @Cf.auth.verify_password
    def verify_password(username_or_token, password):
        # first try to authenticate by token
        # t1 = time.clock()
        user = User.verify_auth_token(username_or_token)
        if not user:
            # 现在不支持用户名密码登录，严重影响时间
            # try to authenticate with username/password
            # user = User.query.filter_by(username=username_or_token).first()
            # if not user or not user.verify_password_only(password):
            #     # print("鉴权花费：%f" % (time.clock() - t1))
            #     return False
            return False
        g.user = user
        # print("鉴权花费：%f" % (time.clock() - t1))
        return True

    def generate_auth_token(self):
        return s.dumps({'id': self.id, 'username': self.username}).decode()

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(Cf.secret_key)
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user


class UserLikes(db.Model):
    __tablename__ = 'UserLikes'
    user_id = Column(Integer, primary_key=True)
    like_user = Column(Integer, primary_key=True)


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

    # 默认返回十条
    @staticmethod
    def get_code(session: Session, user_id: int, offset: int):
        codes: List[Code] = session.query(Code).filter_by(user_id=user_id) \
            .order_by(db.desc(Code.create_date)) \
            .offset(offset) \
            .limit(10) \
            .all()
        return codes

    # 转换为下载地址
    def get_download_url(self):
        from app_utils import AppUtils
        return AppUtils.get_network_url(self.local_path)

    # 读取代码返回
    def read_codes(self) -> str:
        with open(self.local_path, 'r', encoding='utf-8') as f:
            return f.read()

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
    comment_id = Column(Integer, ForeignKey('Comments.id'), nullable=True)  # 发帖id
    title = Column(TINYTEXT)  # 帖子标题
    subtitle = Column(TEXT)  # 副标题，可能作为正文内容
    create_date = Column(DATETIME, default=datetime.now)

    user: User = relationship("User", foreign_keys=[user_id])

    @staticmethod
    def verify_title(title):
        if title is None or type(title) != str or title.strip() == '':
            return False
        return True

    def del_comment(self, comment_id):
        try:
            session = AppUtils.get_session()
            comment = session.query(Comments).filter_by(id=comment_id).first()
            if comment_id == self.comment_id:
                # 对首
                self.comment_id = comment.next_id
                session.delete(comment)
            elif comment.next_id is None:
                # 队尾
                session.delete(comment)
            else:
                # 对中
                pre_comment = session.query(Comments).filter_by(id=comment.parent_id).first()
                next_comment = session.query(Comments).filter_by(id=comment.next_id).first()
                pre_comment.next_id = next_comment.id
                next_comment.parent_id = pre_comment.id
                session.delete(comment)
            session.commit()
            session.close()
            return True
        except Exception as e:
            print(e)
            return False

    def submit_comment(self, comment, session: Session):
        try:
            last_time_commented = Cf.cache.get("comment_" + str(comment.user_id))
            if last_time_commented is not None:
                return False
            Cf.cache.add("comment_" + str(comment.user_id), datetime.now().timestamp(), timeout=10)
            if self.comment_id is None:
                # 对首
                comment.threads_id = self.id
                session.add(comment)
                self.comment_id = comment.id
            else:
                session = AppUtils.get_session()
                # 不是队列首部
                last_comment = session.query(Comments).filter_by(threads_id=self.id, next_id=None).first()
                comment.parent_id = last_comment.id
                session.add(comment)
                last_comment.next_id = comment.id
            return True
        except Exception as e:
            print(e)
            return False

    # comment_id = -1表示从头开始获取,若不为-1的话，则表示从comment_id开始，数10条
    def get_comments(self, comment_id=-1):
        session = AppUtils.get_session()
        try:
            if comment_id == -1:
                comment_id = self.comment_id
            comment = session.query(Comments).filter_by(id=comment_id).first()
            if comment is None:
                return ResponseClass.warn(ResponseCode.COMMENT_NOT_FOUND)
            # 向后获取十条评论
            comments = [comment.get_public_dict()]
            cnt = 1
            while cnt < 10 and comment.next_id is not None:
                n_comment = session.query(Comments).filter_by(id=comment.next_id).first()
                comments.append(n_comment.get_public_dict())
            return comments
        except Exception as e:
            print(e)
            return None
        finally:
            session.close()

    def get_public_dict(self):
        d = dict()
        d['create_date'] = self.create_date
        d['id'] = self.id
        d['title'] = self.title
        d['subtitle'] = self.subtitle
        d['comment_id'] = self.comment_id
        d['username'] = self.user.nickname + '(' + self.user.username + ')'
        d['avatar'] = self.user.avatar_url
        d['user_like'] = self.user.likes
        from app_utils import AppUtils
        session = AppUtils.get_session()
        code = session.query(Code).filter_by(id=self.code_id).first()
        if code is not None:
            d['code_url'] = code.get_download_url()
        else:
            d['code_url'] = ''
        d['user_id'] = self.user_id
        return d


# 评论表
class Comments(db.Model):
    __tablename__ = 'Comments'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 评论ID
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)
    code_id = Column(Integer, ForeignKey('Code.id'), nullable=True)  # 代码ID
    threads_id = Column(Integer, ForeignKey('Threads.id'), nullable=False)  # 帖子ID
    content = Column(TEXT)  # 评论内容
    parent_id = Column(Integer, ForeignKey('Comments.id'), nullable=True)
    next_id = Column(Integer, ForeignKey('Comments.id'), nullable=True)
    # datetime.now指的是插入数据的当前时间，datetime.now()指的是建表时间
    create_date = Column(DATETIME, default=datetime.now)

    user: User = relationship('User', foreign_keys=[user_id])
    parent = relationship('Comments', foreign_keys=[parent_id])
    next = relationship('Comments', foreign_keys=[next_id])
    thread = relationship('Threads', foreign_keys=[threads_id])

    def get_public_dict(self):
        d = dict()
        d['id'] = self.id
        d['user_id'] = self.user_id
        d['threads_id'] = self.threads_id
        d['content'] = self.content
        d['parent_id'] = self.parent_id
        d['next_id'] = self.next_id
        d['create_date'] = self.create_date.timestamp()
        from app_utils import AppUtils
        session = AppUtils.get_session()
        code = session.query(Code).filter_by(id=self.code_id).first()
        if code is not None:
            d['code_url'] = code.get_download_url()
        else:
            d['code_url'] = ''
        d['username'] = self.user.nickname + '(' + self.user.username + ')'
        d['avatar'] = self.user.avatar_url
        return d


# 代码分享表
class CodeSharing(db.Model):
    __tablename__ = 'CodeSharing'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 分享的ID
    user_id = Column(Integer, ForeignKey('User.id'), nullable=False)  # 分享人
    code_id = Column(Integer, ForeignKey('Code.id', ondelete="CASCADE"), nullable=False)  # 本地路径
    like_nums = Column(Integer, default=0)  # 喜欢数
    dislike_nums = Column(Integer, default=0)  # 不喜欢数
    is_private = Column(BOOLEAN, default=True)  # 是否为私有
    credits = Column(Integer)  # 售价，以积分


# 代码购买表
# 需要先增加一条Code记录，再添加新加入代码的code_id
class CodeBought(db.Model):
    __tablename__ = 'CodeBought'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 购买ID
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)  # 购买用户ID
    code_id = Column(Integer, ForeignKey('Code.id', ondelete="CASCADE"), nullable=False)  # 本地路径


# 签到表
class SignIn(db.Model):
    __tablename__ = 'SignIn'
    user_id = Column(Integer, primary_key=True, autoincrement=True)  # 购买ID
    sign_in_time = Column(DATETIME, default=datetime.now)  # 签到时间


# 物品
class Item(db.Model):
    __tablename__ = 'Item'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 物品
    name = Column(String(128))  # 商品名字
    detail = Column(String(1024))  # 商品详情
    credits = Column(Integer)  # 需要点数
    isOn = Column(Boolean, default=True)  # 是否上架
    img = Column(String(255),
                 default="https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=3954745134,"
                         "1665351706&fm=26&gp=0.jpg")  # 图片url


# 购物车
class Cart(db.Model):
    __tablename__ = 'Cart'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 购买ID
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False, primary_key=True)  # 购买用户ID
    item_id = Column(Integer, ForeignKey('Item.id', ondelete="CASCADE"), nullable=False, primary_key=True)  # 本地路径
    create_date = Column(DATETIME, default=datetime.now)

    item = relationship("Item", foreign_keys=[item_id])


# 用户仓库
class Repository(db.Model):
    __tablename__ = 'Repository'
    id = Column(Integer, primary_key=True, autoincrement=True)  # 记录ID
    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"), nullable=False)  # 购买用户ID
    item_id = Column(Integer, ForeignKey('Item.id', ondelete="CASCADE"), nullable=False)  # 本地路径
    create_date = Column(DATETIME, default=datetime.now)

    item = relationship("Item", foreign_keys=[item_id])
