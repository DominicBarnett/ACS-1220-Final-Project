from flask import Flask
from OnePiece_app import db

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)
    # Additional app configurations and extensions setup go here

    return app