from flask import Blueprint, url_for, request, session, redirect
from exts import google_OAuth, db
from datetime import datetime,timedelta
from models import UserModel, AuthModel
import config
#auth
bp = Blueprint("auth", __name__, url_prefix="/auth")


def get_current_user_auth_method():
    user_id = session.get('user_id')

    if user_id is not None:
        # 获取当前用户的认证方法
        auth_method = AuthModel.query.filter_by(user_id=user_id).first()
        return auth_method
    else:
        # 用户未登录或会话已过期
        return None

@bp.route("/login",methods = ['GET', 'POST'])
def login():
    # 假设有方法获取当前用户的认证信息
    auth_method = get_current_user_auth_method()
    if auth_method and auth_method.expires_at <= datetime.utcnow():
        # 令牌过期，尝试使用刷新令牌
        new_token = refresh_access_token(auth_method)
        if new_token:
            return '使用新令牌登录成功' # 跳转到主页
        else:
           print("需要授权")
           return redirect(url_for('auth.google_login'))
            #return '需要重新授权' #跳转到选择登录方式页面
    elif auth_method:
        # 令牌有效，直接登录
        return '直接登录成功' #跳转到主页
    else:
        print("需要授权")
        return redirect(url_for('auth.google_login'))

# Google登录逻辑
google = google_OAuth.register(
    name='google',
    client_id=config.GOOGLE_CLIENT_ID,
    client_secret=config.GOOGLE_CLIENT_SECRET,
    access_token_url=config.GOOGLE_TOKEN_URL,
    access_token_params=config.GOOGLE_ACCESS_TOKEN_PARAMS,
    authorize_url=config.GOOGLE_AUTHORIZE_URL,
    authorize_params=None,
    api_base_url=config.GOOGLE_API_BASE_URL,
    client_kwargs=config.GOOGLE_KWARGS,
    jwks_uri='https://www.googleapis.com/oauth2/v3/certs'
)

@bp.route('/login/google',methods = ['GET','POST'])
def google_login():
    return google.authorize_redirect(url_for('auth.authorize', _external=True))

@bp.route('google/authorize',methods = ['GET', 'POST'])
def authorize():
    code = request.args.get('code')
    state = request.args.get('state')
    # 这里应该有CSRF攻击的防护代码
    try:
        token = google.authorize_access_token()
        print(token)
        user_info = google.get('userinfo').json()
        print("google user_info", user_info)
        # 检查用户是否已存在
        auth_method = AuthModel.query.filter_by(
            provider='google',
            provider_user_id=user_info['email']  # Google的唯一用户ID
        ).first()
        print("auth_method:", auth_method)
        if auth_method:
            user = UserModel.query.get(auth_method.user_id)
            print("user:", user)
            # 更新已有用户的令牌信息
            auth_method.access_token = token['access_token']
            auth_method.refresh_token = token.get('refresh_token')  # 刷新令牌可能不总是返回
            auth_method.expires_at = datetime.utcnow() + timedelta(seconds=token['expires_in'])

            user.updated_at = datetime.now()
            db.session.commit()
            # 更新用户信息（如果需要）
        else:
            # 创建新用户
            user = UserModel(
                username=user_info['name'],
                email=user_info['email'],
                # 其他必要的用户信息
            )
            db.session.add(user)
            db.session.commit()
            print(token['expires_in'], "expires_in add a newer")
            # 创建认证方法
            print("id",user.id)
            print("access-token",token['access_token'])
            print("refreash token", token.get('refresh_token'))
            print("expire time", datetime.utcnow() + timedelta(seconds=token['expires_in']))
            auth_method = AuthModel(
                provider='google',
                provider_user_id=user_info['email'],
                user_id=user.id,
                access_token=token['access_token'],
                refresh_token=token.get('refresh_token'),
                expires_at=datetime.utcnow() + timedelta(seconds=token['expires_in']),
                # 存储其他认证相关信息，如token
            )
            db.session.add(auth_method)
            db.session.commit()

            # 在这里，您可以设置session或其他登录状态
            session['user_id'] = user.id
            return '登录成功'  # 跳转到主页
    except Exception as e:
        # 错误处理
        return '认证失败'

# 令牌刷新逻辑
def is_token_expired(auth_model):
    return datetime.utcnow() >= auth_model.expires_at

def refresh_access_token(auth_model):
    if auth_model.refresh_token & auth_model.provider == "google":
        # 向Google发送请求以刷新访问令牌
        # 这通常需要使用OAuth库或直接发起HTTP请求
        # 假设`refresh_google_token`是执行此操作的函数
        new_token_info = refresh_google_token(auth_model.refresh_token)

        # 更新数据库中的令牌信息
        auth_model.access_token = new_token_info['access_token']
        auth_model.expires_at = datetime.utcnow() + timedelta(seconds=new_token_info['expires_in'])
        db.session.commit()


def refresh_google_token(refresh_token):
    # Google的令牌刷新端点
    refresh_url = 'https://oauth2.googleapis.com/token'
    # 准备请求数据
    refresh_payload = {
        'client_id': config.GOOGLE_CLIENT_ID,
        'client_secret': config.GOOGLE_CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }

    # 向Google发送POST请求
    response = request.post(refresh_url, data=refresh_payload)

    if response.status_code == 200:
        # 解析响应数据
        new_token_info = response.json()
        return new_token_info
    else:
        # 处理错误情况
        print("Failed to refresh token: ", response.text)
        return None

@bp.route('/login/wechat')
def wechat_login():
    # 微信登录逻辑
    pass


@bp.route('/login/qq')
def qq_login():
    # QQ登录逻辑
    pass

