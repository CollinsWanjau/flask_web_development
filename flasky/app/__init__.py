from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    app = Flask(__name__)

    """
    The config settings stored in one of the classes defined in config.py
    can be imported directly nito the app using from_object()
    """
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    

    # Initialize extensions
    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    # attach routes and custom error pagaes here


    # Blueprint registration
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Blueprint attachment
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
