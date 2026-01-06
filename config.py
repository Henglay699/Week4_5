import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "mysql+pymysql://root:Henglay699$@localhost:3306/user_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    