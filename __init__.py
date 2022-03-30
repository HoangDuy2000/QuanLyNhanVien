from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_login import LoginManager
import cloudinary


app = Flask(__name__)

app.secret_key = 'sfdafawfaw124124asfafafa'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/quanlynhasach?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

babel = Babel(app=app)
@babel.localeselector
def get_locale():
    return 'vi'

cloudinary.config(
    cloud_name = 'dpolbadt9',
    api_key = '565418183598838',
    api_secret = 'bd6GxWSU-GJEGggO2TrMu2DzimA',
)