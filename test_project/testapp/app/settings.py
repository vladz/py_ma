import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = os.getenv('DEBUG', False)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI",
                                        "sqlite:///project.db")
