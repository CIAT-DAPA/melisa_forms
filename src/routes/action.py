from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from melisa_orm.models.form import Form
from melisa_orm import Track
from melisa_orm.models.actions import Action,ActionRequestEnum
from datetime import datetime
from flask_login import current_user
action_bp = Blueprint('action', __name__)

@action_bp.route('/actions')
@login_required
def show_action():
    action = Action.objects()
    form= Form.objects(track__enable=True)
    return render_template('action.html', action=action,form=form,actionsenum=ActionRequestEnum)
@action_bp.route('/addaction')
@login_required
def addd_action():
    form= Form.objects(track__enable=True)
    return render_template('addaction.html',form=form,actionsenum=ActionRequestEnum)

@action_bp.route('/action/add', methods=['POST'])
@login_required
def add_action():
    track=Track(user=current_user.get_id(),created=datetime.now(), updated=datetime.now,enable=True) #user will be replace with the current user
    name = request.form['name']
    formu = request.form['formu']
    call_url = request.form['callurl']
    request_data = request.form['request']
    track = track
    action = Action(name=name, call_url=call_url,request=request_data,track=track,form=formu)
    action.save()
    flash("action added succesfully")
    return redirect('/action')

@action_bp.route('/editaction/<string:action_id>', methods=['GET', 'POST'])
@login_required
def edit_action(action_id):
    action = Action.objects(id=action_id).first()
    form= Form.objects(track__enable=True)

 
    
    if request.method == 'POST':
        name = request.form['name']
        formu = request.form['formu']
        call_url = request.form['callurl']
        request_data = request.form['request']
        track = action.track
        track['updated'] = datetime.now()
        track['user'] = current_user.get_id()  
        action = Action(name=name, call_url=call_url,request=request_data,track=track,form=formu)

        flash("action updated successfully")
        return redirect('/action')

    return render_template('editaction.html', action=action,form=form,actionsenum=ActionRequestEnum)

@action_bp.route('/deleteaction/<string:action_id>')
@login_required
def delete_action(action_id):
    action = Action.objects(id=action_id).first()

    if action:
        track = action.track

        track['enable'] = False
        track['user'] = current_user.get_id()
        action.update(track=track)
        flash("action deleted successfully")
    else:
        flash("action not found")

    return redirect('/action')

@action_bp.route('/resetaction/<string:action_id>')
@login_required
def reset_action(action_id):
    action = Action.objects(id=action_id).first()

    if action:
        track = action.track

        track['enable'] = True
        track['user'] = current_user.get_id()
        action.update(track=track)
        flash("action recover successfully")
    else:
        flash("action not found")

    return redirect('/action')


@action_bp.errorhandler(401)
def unauthorized_handler(error):
    return render_template('error.html'), 401


