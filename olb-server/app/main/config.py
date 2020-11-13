# config file for different app versions
# mostly for test vs dev but we might want prod one day
import os

base_directory = os.path.abspath(os.path.dirname(__file__))


# Default config class
class Config:
    JWT_SECRET_KEY = os.getenv("OLB_SECRET_KEY", "joel is great")  # secret key for jwt encoding, set this in environment variables
    JWT_ACCESS_TOKEN_EXPIRES = False  # Access tokens don't expire, change this before monetizing this program lmao
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access"]
    DEBUG = False


# App config for dev version
class Dev_Config(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(base_directory, 'olb_dev.db')}"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:example@localhost:5432/olb_dev"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


# App config for unit test version
class Test_Config(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(base_directory, 'olb_test.db')}"
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
