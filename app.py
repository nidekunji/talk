from flask import Flask, session, g
import config
from exts import db, mail, google_OAuth
from flask_migrate import Migrate
from blueprints.auth import bp as auth_bp
from models import UserModel

app = Flask(__name__)
app.secret_key = ""
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
google_OAuth.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(auth_bp)


# before_request / before_first_request / after_request
# hook
@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
    else:
        setattr(g, "user", None)


@app.context_processor
def my_context_processor():
    return {"user": g.user}



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'




if __name__ == '__main__':
    app.run()
