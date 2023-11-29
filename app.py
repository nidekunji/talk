from flask import Flask
import config
from exts import db, mail, google_OAuth
from flask_migrate import Migrate
from blueprints.auth import bp as auth_bp

app = Flask(__name__)
app.secret_key = ""
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
google_OAuth.init_app(app)
migrate = Migrate(app, db)
app.register_blueprint(auth_bp)




@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
