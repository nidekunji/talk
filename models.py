from exts import db
from datetime import datetime

class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200)) #密码的哈希值（如果提供了密码登录）。
    email = db.Column(db.String(100)) #用户的主要电子邮件地址，可选。
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now)


class AuthModel(db.Model):
    __tablename__ = "auth_methods"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(200), nullable=False)
    provider = db.Column(db.String(100), nullable=False)
    provider_user_id = db.Column(db.String(200), nullable=False)
    provider_data =  db.Column(db.String(200))
    access_token = db.Column(db.String(255))
    refresh_token = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime)  # 访问令牌的过期时间
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(UserModel, backref="auth_methods")

class ProfilesModel:
    __tablename__ = "user_profiles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    profile_picture = db.Column(db.String(200))
    # 外键
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(UserModel, backref="profile")