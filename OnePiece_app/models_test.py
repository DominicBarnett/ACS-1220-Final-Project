from dotenv import load_dotenv
load_dotenv()
import os
import pytest
from sqlalchemy.exc import IntegrityError
from flask import Flask
from OnePiece_app import db, app
from OnePiece_app.models import Affiliation, Character, User




@pytest.fixture(scope='module')
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

def test_user_creation(client):
    user = User(username="test_user", password="password123")
    db.session.add(user)
    db.session.commit()
    assert user.id is not None
    assert user.username == "test_user"
    assert user.password == "password123"

def test_affiliation_creation(client):
    affiliation = Affiliation(title="Straw Hat Pirates")
    db.session.add(affiliation)
    db.session.commit()
    assert affiliation.id is not None
    assert affiliation.title == "Straw Hat Pirates"

def test_character_creation(client):
    affiliation = Affiliation(title="Straw Hat Pirates")
    db.session.add(affiliation)
    db.session.commit()
    character = Character(name="Monkey D. Luffy", affiliation=affiliation)
    db.session.add(character)
    db.session.commit()
    assert character.id is not None
    assert character.name == "Monkey D. Luffy"
    assert character.affiliation == affiliation
