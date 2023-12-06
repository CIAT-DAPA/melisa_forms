from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from melisa_orm.models.form import Form
from melisa_orm import Track,Validation, Melisa
from melisa_orm.models.melisa import Melisa
from datetime import datetime

melisa_bp = Blueprint('melisa', __name__)
@melisa_bp.route('/melisa')
def show_melisa():
    melisa = Melisa.objects()
    return render_template('melisa.html', melisa=melisa)
@melisa_bp.route('/addmelisa')
def addd_melisa():
    boolvalues=[True,False]

    return render_template('add_melisa.html',melisabool=boolvalues)

@melisa_bp.route('/melisa/add', methods=['POST'])
def add_melisa():
    form_data = request.form

    name = form_data['name']
    url_post = form_data['urlpost']
    token = form_data['token']
    say_hi = form_data['sayhi'] == 'True' 
    say_wait = form_data['saywait'] == 'True'  
    countries = form_data.getlist('countries[]')
    


    melisa = Melisa(
        name=name,
        url_post=url_post,
        token=token,
        say_hi=say_hi,
        say_wait=say_wait,
        countries=countries,
    )

    melisa.save()

    flash("Melisa added successfully")
    return redirect('/melisa')
@melisa_bp.route('/editmelisa/<string:melisa_id>', methods=['GET', 'POST'])
def edit_melisa(melisa_id):
    boolvalues=[True,False]

    melisa = Melisa.objects(id=melisa_id).first()

    if request.method == 'POST':
        form_data = request.form

        validation_names = form_data.getlist('validation_name[]')
        validation_exps = form_data.getlist('validation_exp[]')
        validation_error_msgs = form_data.getlist('validation_error_msg[]')

        validations = [Validation(name=name, exp=exp, error_msg=error_msg) for name, exp, error_msg in zip(validation_names, validation_exps, validation_error_msgs)]

        melisa.update(
            form=Form.objects.get(id=form_data['formu']),
            name=form_data['name'],
            description=form_data['description'],
            order=int(form_data['order']),
            validations=validations,
            track__user='user yo', 
            track__updated=datetime.now() 
        )



        flash("melisa updated successfully")
        return redirect('/melisa')

    return render_template('edit_melisa.html', melisa=melisa,melisabool=boolvalues)

@melisa_bp.route('/deletemelisa/<string:melisa_id>')
def delete_melisa(melisa_id):
    melisa = melisa.objects(id=melisa_id).first()

    if melisa:
        track = melisa.track

        track['enable'] = False
        track['user'] = 'deleted by yo'
        melisa.update(track=track)
        flash("melisa deleted successfully")
    else:
        flash("melisa not found")

    return redirect('/melisa')

@melisa_bp.route('/resetmelisa/<string:melisa_id>')
def reset_melisa(melisa_id):
    melisa = melisa.objects(id=melisa_id).first()

    if melisa:
        track = melisa.track

        track['enable'] = True
        track['user'] = 'recover by yo'
        melisa.update(track=track)
        flash("melisa recover successfully")
    else:
        flash("melisa not found")

    return redirect('/melisa')