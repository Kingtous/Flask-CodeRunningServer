import appConfig

# db
db = appConfig.AppBaseConfig.database


class User(appConfig.AppBaseConfig.database.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nickname = db.Column(db.String(20), nullable=False)
    # 密码用32位MD5码值存储
    password = db.Column(db.String(32), nullable=False)

