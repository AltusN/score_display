import os
base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY=os.environ.get("SECRET_KEY") or "secret"
    #Database
    SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(base_dir, "score_display.db")
    SQLALCHEMY_TRACK_MODIFICATIONS=False