from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from melisa_orm.models.form import Form
from melisa_orm import Track,Validation, Melisa
from melisa_orm.models.melisa import Melisa
from datetime import datetime
from flask_login import current_user
melisa_bp = Blueprint('melisa', __name__)
@melisa_bp.route('/melisa')
@login_required

def show_melisa():
    melisa = Melisa.objects()
    return render_template('melisa.html', melisa=melisa)
@melisa_bp.route('/addmelisa')
@login_required
def addd_melisa():
    boolvalues=[True,False]

    return render_template('add_melisa.html',melisabool=boolvalues)

@melisa_bp.route('/melisa/add', methods=['POST'])
@login_required
def add_melisa():
    track=Track(user=current_user.get_id(),created=datetime.now(), updated=datetime.now,enable=True)
    form_data = request.form
    name = form_data['name']
    url_post = form_data['urlpost']
    token = form_data['token']
    say_hi = form_data['sayhi'] == 'True' 
    say_wait = form_data['saywait'] == 'True'  
    countries = form_data.getlist('countries[]') if 'countries[]' in form_data else ['']
    



    melisa = Melisa(
        name=name,
        url_post=url_post,
        token=token,
        say_hi=say_hi,
        say_wait=say_wait,
        countries=countries,
        track=track
    )

    melisa.save()

    flash("Melisa added successfully")
    return redirect('/melisa')
@melisa_bp.route('/editmelisa/<string:melisa_id>', methods=['GET', 'POST'])
@login_required
def edit_melisa(melisa_id):
    boolvalues=[True,False]

    melisa = Melisa.objects(id=melisa_id).first()

    if request.method == 'POST':

        form_data = request.form
        name = form_data['name']
        url_post = form_data['urlpost']
        token = form_data['token']
        say_hi = form_data['sayhi'] == 'True' 
        say_wait = form_data['saywait'] == 'True'  
        countries = form_data.getlist('countries[]') if 'countries[]' in form_data else ['']
        track = melisa.track

        track['enable'] = True
        track['user'] = current_user.get_id()
        track['updated'] = datetime.now()
        melisa.update(
            name=name,
            url_post=url_post,
            token=token,
            say_hi=say_hi,
            say_wait=say_wait,
            countries=countries,
            track=track
        )
        flash("melisa updated successfully")
        return redirect('/melisa')

    return render_template('edit_melisa.html', melisa=melisa,melisabool=boolvalues)

@melisa_bp.route('/deletemelisa/<string:melisa_id>')
@login_required
def delete_melisa(melisa_id):
    melisa = Melisa.objects(id=melisa_id).first()

    if melisa:
        track = melisa.track

        track['enable'] = False
        track['updated'] = datetime.now()
        track['user'] = current_user.get_id()
        melisa.update(track=track)
        flash("melisa deleted successfully")
    else:
        flash("melisa not found")

    return redirect('/melisa')

@melisa_bp.route('/resetmelisa/<string:melisa_id>')
@login_required
def reset_melisa(melisa_id):
    melisa = Melisa.objects(id=melisa_id).first()

    if melisa:
        track = melisa.track

        track['enable'] = True
        track['updated'] = datetime.now()
        track['user'] = current_user.get_id()
        melisa.update(track=track)
        flash("melisa recover successfully")
    else:
        flash("melisa not found")

    return redirect('/melisa')

@melisa_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401