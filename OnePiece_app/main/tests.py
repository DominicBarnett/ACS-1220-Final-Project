import os
import unittest
from flask_testing import TestCase
from OnePiece_app.main import create_app, db
from OnePiece_app.models import User, Character, Affiliation, AffiliationCategory, DevilFruitCategory, HakiCategory

class ModelsTestCase(TestCase):
    def create_app(self):
        return create_app(config_name="testing")

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_creation(self):
        user = User(username="test_user", password="test_password")
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(user.id)

    def test_affiliation_creation(self):
        affiliation = Affiliation(title="Test Affiliation")
        db.session.add(affiliation)
        db.session.commit()
        self.assertIsNotNone(affiliation.id)

    def test_character_creation(self):
        affiliation = Affiliation(title="Test Affiliation")
        user = User(username="test_user", password="test_password")
        db.session.add_all([affiliation, user])
        db.session.commit()
        character = Character(name="Test Character", affiliation=affiliation, created_by=user)
        db.session.add(character)
        db.session.commit()
        self.assertIsNotNone(character.id)

    def test_favorite_characters_association(self):
        affiliation = Affiliation(title="Test Affiliation")
        user = User(username="test_user", password="test_password")
        character = Character(name="Test Character", affiliation=affiliation, created_by=user)
        user.favorite_characters_list.append(character)
        db.session.add_all([affiliation, user, character])
        db.session.commit()
        self.assertIn(character, user.favorite_characters_list)

if __name__ == '__main__':
    unittest.main()