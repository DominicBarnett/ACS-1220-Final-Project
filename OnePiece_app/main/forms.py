from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, SubmitField, SelectMultipleField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange
from OnePiece_app.models import AffiliationCategory, Affiliation, Character, DevilFruitCategory, HakiCategory

class AffiliationForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""
    title = StringField('Affiliation',
        validators=[
            DataRequired(),
            Length(min=3, max=80, message="Your message needs to be between 3 and 80 characters long.")
        ])
    submit = SubmitField('Submit')

class CharactersForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('Character Name',
                       validators=[
                           DataRequired(),
                           Length(min=3, max=80, message="Your message needs to be between 3 and 80 characters long.")
                       ])
    category = SelectField('Category', choices=AffiliationCategory.choices())
    affiliation = QuerySelectField('affiliation', query_factory=lambda: Affiliation.query.all(), get_label='title')
    devil_fruit = SelectField('Category', choices=DevilFruitCategory.choices())
    haki = SelectField('Category', choices=HakiCategory.choices())
    submit = SubmitField('Submit') 
