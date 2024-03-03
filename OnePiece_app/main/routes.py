from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_login import login_required, current_user
from OnePiece_app.models import Affiliation, Character, User, CharacterWithDevilFruit, CharacterWithHaki
from OnePiece_app.main.forms import AffiliationForm, CharactersForm
from OnePiece_app.extensions import db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_affiliations = Affiliation.query.all()
    all_haki_characters = Character.query.filter(Character.haki != 'No').all()
    all_devilfruit_characters = Character.query.filter(Character.devil_fruit != 'No').all()
    print(current_user)
    return render_template('home.html', all_affiliations=all_affiliations,
                            all_haki_characters=all_haki_characters, 
                            all_devilfruit_characters=all_devilfruit_characters)

@main.route('/new_affiliation', methods=['GET', 'POST'])
@login_required
def new_affiliation():
    form = AffiliationForm()
    if form.validate_on_submit():
        new_affiliation = Affiliation(
            title=form.title.data,
            created_by_id=current_user.id
        )
        db.session.add(new_affiliation)
        db.session.commit()

        flash('New affiliation was created successfully.')
        # Pass the new_affiliation variable to the template context
        return redirect(url_for('main.affiliation_detail', affiliation_id=new_affiliation.id))
    return render_template('new_affiliation.html', form=form)

@main.route('/new_character', methods=['GET', 'POST'])
@login_required
def new_character():
    form = CharactersForm()
    if form.validate_on_submit():
        new_character = Character(
            name=form.name.data,
            category=form.category.data,
            affiliation=form.affiliation.data,
            devil_fruit=form.devil_fruit.data,
            haki=form.haki.data,
            created_by_id=current_user.id
        )
        db.session.add(new_character)
        db.session.commit()

        flash('New character was created successfully.')
        return redirect(url_for('main.character_detail', character_id=new_character.id))
    return render_template('new_character.html', form=form)

@main.route('/affiliation/<affiliation_id>', methods=['GET', 'POST'])
@login_required
def affiliation_detail(affiliation_id):
    affiliation = Affiliation.query.get(affiliation_id)
    form = AffiliationForm(obj=affiliation)
    
    # Check if new_affiliation is passed in the request args
    new_affiliation = None
    if 'new_affiliation' in request.args:
        new_affiliation_id = request.args.get('new_affiliation')
        new_affiliation = Affiliation.query.get(new_affiliation_id)
    
    if form.validate_on_submit():
        affiliation.affiliation_name = form.title.data
        db.session.commit()

        flash('Affiliation was updated successfully.')
        return redirect(url_for('main.affiliation_detail', affiliation_id=affiliation.id))
    
    # Pass new_affiliation to the template context
    return render_template('affiliation_detail.html', affiliation=affiliation, form=form, new_affiliation=new_affiliation)
@main.route('/characters/<character_id>', methods=['GET', 'POST'])
@login_required
def character_detail(character_id):
    character = Character.query.get(character_id)
    form = CharactersForm(obj=character)
    if form.validate_on_submit():
        character.name = form.name.data
        character.category = form.category.data
        character.affiliation = form.affiliation.data
        db.session.commit()

        flash('Character was updated successfully.')
        return redirect(url_for('main.character_detail', character_id=character.id))
    return render_template('character_detail.html', character=character, form=form)

@main.route('/add_to_favorite_character_list/<character_id>', methods=['POST'])
@login_required
def add_to_favorite_characters_list(character_id):
    character = Character.query.get(character_id)
    if character in current_user.favorite_characters_list_items:
        flash("Character already in favorite characters list.")
        return redirect(url_for('main.character_detail', character_id=character.id))
    current_user.favorite_characters_list_items.append(character)
    db.session.commit()
    flash("Character added to favorite characters list successfully.")
    return redirect(url_for('main.character_detail', character_id=character.id))

@main.route('/delete_from_favorite_characters_list/<character_id>', methods=['POST'])
@login_required
def delete_from_favorite_characters_list(character_id):
    character = Character.query.get(character_id)
    if character in current_user.favorite_characters_list_items:
        current_user.favorite_characters_list_items.remove(character)
        db.session.commit()
        flash("Character removed from favorite characters list successfully.")
    return redirect(url_for('main.favorite_characters_list'))

@main.route('/favorite_characters_list')
@login_required
def favorite_characters_list():
    user_characters_list = current_user.favorite_characters_list_items
    return render_template('favorite_characters_list.html', character_list=user_characters_list)