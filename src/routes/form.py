from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from melisaORM.models.form import Form,Track
from datetime import datetime

form_bp = Blueprint('form', __name__)

@form_bp.route('/form')
def show_form():
    form = Form.objects()
    return render_template('form.html', form=form)
@form_bp.route('/addform')
def addd_form():
    form = Form.objects()
    return render_template('addform.html', form=form)

@form_bp.route('/form/add', methods=['POST'])
def add_form():
    track=Track(user='user',created=datetime.now(), updated=datetime.now,enable=True) #user will be replace with the current user
    name = request.form['name']
    command = request.form['command']
    track = track
    form = Form(name=name, command=command,track=track)
    form.save()
    flash("form added succesfully")
    return redirect('/form')

@form_bp.route('/edit/<string:form_id>', methods=['GET', 'POST'])
def edit_form(form_id):
    form = Form.objects(id=form_id).first()
    """ json_data = [{"id":str(x.id),"name":x.name,"ext_id":x.ext_id} for x in form] """
    
    if request.method == 'POST':
        name = request.form['name']
        command = request.form['command']
        track = form.track
        track['updated'] = datetime.now()
        track['user'] = 'fui yo ahora' #it will be replace with the current user
        form.update(name=name, command=command, track=track)

        flash("form updated successfully")
        return redirect('/form')

    return render_template('edit_form.html', form=form)

@form_bp.route('/delete/<string:form_id>')
def delete_form(form_id):
    form = Form.objects(id=form_id).first()

    if form:
        track = form.track

        track['enable'] = False
        track['user'] = 'deleted by yo'
        form.update(track=track)
        flash("form deleted successfully")
    else:
        flash("form not found")

    return redirect('/form')

@form_bp.route('/reset/<string:form_id>')
def reset_form(form_id):
    form = Form.objects(id=form_id).first()

    if form:
        track = form.track

        track['enable'] = True
        track['user'] = 'recover by yo'
        form.update(track=track)
        flash("form recover successfully")
    else:
        flash("form not found")

    return redirect('/form')



