import os
from dotenv import load_dotenv
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'picaso420'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    IMAGINESTUDIOS_MAIL_SUBJECT_PREFIX = '[Imagine]'
    IMAGINESTUDIOS_MAIL_SENDER = 'Imagine Admin <tripperskripper@gmail.com>'
    IMAGINE_ADMIN = os.environ.get('IMAGINE_ADMIN')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    IMAGINE_POSTS_PER_PAGE = os.environ.get('IMAGINE_POSTS_PER_PAGE')
    IMAGINE_FOLLOWERS_PER_PAGE = 50
    """
    Configuration classes define a init_app() class method that takes an
    application instance as an arg
    """
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}

