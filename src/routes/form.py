from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from melisa_orm.models.form import Form,Track
from datetime import datetime
from flask_login import current_user
form_bp = Blueprint('form', __name__)

@form_bp.route('/form')
@login_required
def show_form():
    form = Form.objects()
    return render_template('form.html', form=form)
@form_bp.route('/addform')
def addd_form():
    form = Form.objects()
    return render_template('addform.html', form=form)

@form_bp.route('/form/add', methods=['POST'])
@login_required
def add_form():
    track=Track(user=current_user.get_id(),created=datetime.now(), updated=datetime.now,enable=True) #user will be replace with the current user
    name = request.form['name']
    command = request.form['command']
    ext_id = request.form['ext_id']
    track = track
    form = Form(name=name, command=command,track=track,ext_id=ext_id)
    form.save()
    flash("form added succesfully")
    return redirect('/form')

@form_bp.route('/edit/<string:form_id>', methods=['GET', 'POST'])
@login_required
def edit_form(form_id):
    form = Form.objects(id=form_id).first()
    
    if request.method == 'POST':
        name = request.form['name']
        command = request.form['command']
        ext_id = request.form['ext_id']

        track = form.track
        track['updated'] = datetime.now()
        track['user'] = current_user.get_id() #it will be replace with the current user
        form.update(name=name, command=command, track=track,ext_id=ext_id)

        flash("form updated successfully")
        return redirect('/form')

    return render_template('edit_form.html', form=form)

@form_bp.route('/delete/<string:form_id>')
@login_required
def delete_form(form_id):
    form = Form.objects(id=form_id).first()

    if form:
        track = form.track

        track['enable'] = False
        track['user'] = current_user.get_id()
        form.update(track=track)
        flash("form deleted successfully")
    else:
        flash("form not found")

    return redirect('/form')

@form_bp.route('/reset/<string:form_id>')
@login_required
def reset_form(form_id):
    form = Form.objects(id=form_id).first()

    if form:
        track = form.track

        track['enable'] = True
        track['user'] = current_user.get_id()
        form.update(track=track)
        flash("form recover successfully")
    else:
        flash("form not found")

    return redirect('/form')

@form_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401

