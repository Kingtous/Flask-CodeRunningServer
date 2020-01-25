from flask import g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer

import appConfig as Cf

# db
db = Cf.database
auth = HTTPBasicAuth()


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
