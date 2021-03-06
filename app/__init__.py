from flask import Flask
from flask_bootstrap import Bootstrap
from flask_kvsession import KVSessionExtension
from flask_migrate import Migrate
# from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from simplekv.fs import FilesystemStore

from config import config

store = FilesystemStore('./data/session')
kvsession = KVSessionExtension()

bootstrap = Bootstrap()
# mail = Mail()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    kvsession.init_app(app, session_kvstore=store)
    bootstrap.init_app(app)
    # mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
