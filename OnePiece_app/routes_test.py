import pytest
from flask import url_for
from OnePiece_app.main import create_app
from OnePiece_app.extensions import db
from OnePiece_app.models import Affiliation, Character, User


@pytest.fixture
def app():
    app = create_app('config.TestingConfig')
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()


def test_homepage(client, init_database):
    response = client.get('/')
    assert response.status_code == 200


def test_new_affiliation(client, init_database):
    response = client.post('/new_affiliation', data=dict(title='New Affiliation'), follow_redirects=True)
    assert response.status_code == 200
    assert b'New affiliation was created successfully.' in response.data


def test_new_character(client, init_database):
    response = client.post('/new_character', data=dict(name='New Character', category='Pirate', affiliation='Straw Hat Pirates', devil_fruit='No', haki='Yes'), follow_redirects=True)
    assert response.status_code == 200
    assert b'New character was created successfully.' in response.data


def test_affiliation_detail(client, init_database):
    affiliation = Affiliation(title='Test Affiliation')
    db.session.add(affiliation)
    db.session.commit()
    response = client.get(f'/affiliation/{affiliation.id}')
    assert response.status_code == 200


def test_character_detail(client, init_database):
    character = Character(name='Test Character', category='Pirate', affiliation='Straw Hat Pirates', devil_fruit='No', haki='Yes')
    db.session.add(character)
    db.session.commit()
    response = client.get(f'/characters/{character.id}')
    assert response.status_code == 200


def test_favorite_characters_list(client, init_database):
    user = User(username='test_user', email='test@example.com', password='password')
    db.session.add(user)
    db.session.commit()
    client.post('/login', data=dict(username='test_user', password='password'), follow_redirects=True)
    response = client.get('/favorite_characters_list')
    assert response.status_code == 200