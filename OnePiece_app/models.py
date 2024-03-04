from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy_utils import URLType
from flask_login import UserMixin
from OnePiece_app import db
from OnePiece_app.utils import FormEnum

class AffiliationCategory(FormEnum):
    """Categories of Affiliations."""
    PIRATE = 'Pirate'
    MARINE = 'Marine'
    REVOLUTIONARY = 'Revolutionary'
    CIVILIAN = 'Civilian'
    OTHER = 'Other'

class DevilFruitCategory(FormEnum):
    """Categories of Devil Fruit"""
    PARAMECIA = 'Paramecia'
    ZOAN = 'Zoan'
    LOGIA = 'Logia'
    No = 'No'

class HakiCategory(FormEnum):
    """Categories of Devil Fruit"""
    CONQUERORS = 'Conquerors'
    OBSERVATION = 'Observation'
    ARMAMENT = 'Armament'
    CONQUERORSandOBSERVATION = 'Conquerors and Observation'
    CONQUERORSandARMAMENT = 'Conquerors and Armament'
    OBSERVATIONandARMAMENT = 'Observation and Armament'
    ALLTYPES = 'All types'
    No = 'No'

class Affiliation(db.Model):
    """Affiliation model. What group a given created character is apart of"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    characters = db.relationship('Character', back_populates='affiliation')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

    def __str__(self):
        return self.affiliation_name

    def __repr__(self):
        return self.affiliation_name
    
class Character(db.Model):
    """Characters model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    category = db.Column(db.Enum(AffiliationCategory), default=AffiliationCategory.OTHER)
    affiliation_id = db.Column(
        db.Integer, db.ForeignKey('affiliation.id'), nullable=False)
    affiliation = db.relationship('Affiliation', back_populates='characters')
    devil_fruit = db.Column(db.Enum(DevilFruitCategory), default=DevilFruitCategory.No)
    haki = db.Column(db.Enum(HakiCategory), default=HakiCategory.No)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    favorite_characters_list = db.relationship(
        "User", secondary="favorite_characters_list_table", back_populates="favorite_characters_list_items")
    devil_fruit_entry = db.relationship("CharacterWithDevilFruit", back_populates="character")
    haki_entry = db.relationship("CharacterWithHaki", back_populates="character")


    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name
    
class User(UserMixin, db.Model):
    """User model."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

    favorite_characters_list_items = db.relationship('Character', secondary="favorite_characters_list_table", back_populates='favorite_characters_list') 

favorite_characters_list_table = db.Table('favorite_characters_list_table',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('character_id', db.Integer, db.ForeignKey('character.id')),
    db.PrimaryKeyConstraint('user_id', 'character_id')
)
class CharacterWithDevilFruit(db.Model):
    __tablename__ = 'characters_with_devil_fruit'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship('Character', back_populates='devil_fruit_entry')

class CharacterWithHaki(db.Model):
    __tablename__ = 'characters_with_haki'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'))
    character = db.relationship('Character', back_populates='haki_entry')