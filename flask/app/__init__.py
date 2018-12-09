import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"
bootstrap = Bootstrap(app)
moment = Moment(app)

from app import routes, models, errors


if not app.debug:
    if not os.path.exists("logs"):
        os.mkdir("logs")
    fh = RotatingFileHandler("logs/app.log", maxBytes=10240, backupCount=10)
    fh.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    fh.setLevel(logging.INFO)
    app.logger.addHandler(fh)

    app.logger.setLevel(logging.INFO)
    app.logger.info("App startup")
