from pathlib import Path

basedir = Path(__file__).parent.parent

class Baseconfig:
    SECRET_KEY = "2AZSMsspbcY2hBsJ"
    WTF_CSRF_SECRET_KEY="AuwzyszU5sugKN7KZs6f"

class LocalConfig(Baseconfig):
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=True

class TestingConfig(Baseconfig):
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False

config = {
    "testing": TestingConfig,
    "local": LocalConfig,
}