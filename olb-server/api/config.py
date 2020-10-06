# config file for different app versions
# mostly for test vs dev but we might want prod one day
import os

base_directory = os.path.abspath(os.path.dirname(__file__))


# Default config class
class Config:
    SECRET_KEY = os.getenv('OLB_SECRET_KEY', 'joel is great')  # secret key for jwt encoding, set this in environment variables
    DEBUG = False


# App config for dev version
class Dev_Config(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(base_directory, "olb_dev.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# App config for unit test version
class Test_Config(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(base_directory, "olb_test.db")}'
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# App config for prod version
class Prod_Config(Config):
    DEBUG = False
    # set the sqlalchemy uri to a postgres or mysql or whatever


configs = dict(
    dev=Dev_Config,
    test=Test_Config,
    prod=Prod_Config
)

key = Config.SECRET_KEY
