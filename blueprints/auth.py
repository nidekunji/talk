from flask import Blueprint, url_for, request
from exts import google_OAuth
from authlib.integrations.flask_client import OAuth
import config
#auth
bp = Blueprint("auth", __name__, url_prefix="/auth")

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

@bp.route('/login/google',methods = ['GET', 'POST'])
def google_login():
    return google.authorize_redirect(url_for('auth.authorize', _external=True))

@bp.route('google/authorize',methods = ['GET', 'POST'])
def authorize():
    code = request.args.get('code')
    state = request.args.get('state')

    # 确认state参数以防止CSRF攻击
    # ...

    # 使用code换取访问令牌
    try:
        token = google.authorize_access_token()
        # 使用token获取用户信息
        user_info = google.get('userinfo').json()
        # ...
        return '登录成功'
    except Exception as e:
        # 错误处理
        return '认证失败'
    # token = google.authorize_access_token()
    # user_info = google.get('userinfo').json()
    # # 在这里，你可以保存用户信息到数据库
    # # user_info 包含用户的Google个人信息
    # return f'登录成功！<br>{user_info}'

@bp.route('/login/wechat')
def wechat_login():
    # 微信登录逻辑
    pass

@bp.route('/login/qq')
def qq_login():
    # QQ登录逻辑
    pass

