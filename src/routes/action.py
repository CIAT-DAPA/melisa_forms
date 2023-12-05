from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from melisa_orm.models.form import Form
from melisa_orm import Track
from melisa_orm.models.actions import Action,ActionRequestEnum
from datetime import datetime

action_bp = Blueprint('action', __name__)

@action_bp.route('/action')
def show_action():
    action = Action.objects()
    form= Form.objects(track__enable=True)
    return render_template('action.html', action=action,form=form,actionsenum=ActionRequestEnum)
@action_bp.route('/addaction')
def addd_action():
    form= Form.objects(track__enable=True)
    return render_template('addaction.html',form=form,actionsenum=ActionRequestEnum)

@action_bp.route('/action/add', methods=['POST'])
def add_action():
    track=Track(user='user',created=datetime.now(), updated=datetime.now,enable=True) #user will be replace with the current user
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
        track['user'] = 'fui yo ahora'  # it will be replaced with the current user
        action = Action(name=name, call_url=call_url,request=request_data,track=track,form=formu)

        flash("action updated successfully")
        return redirect('/action')

    return render_template('editaction.html', action=action,form=form,actionsenum=ActionRequestEnum)

@action_bp.route('/deleteaction/<string:action_id>')
def delete_action(action_id):
    action = Action.objects(id=action_id).first()

    if action:
        track = action.track

        track['enable'] = False
        track['user'] = 'deleted by yo'
        action.update(track=track)
        flash("action deleted successfully")
    else:
        flash("action not found")

    return redirect('/action')

@action_bp.route('/resetaction/<string:action_id>')
def reset_action(action_id):
    action = Action.objects(id=action_id).first()

    if action:
        track = action.track

        track['enable'] = True
        track['user'] = 'recover by yo'
        action.update(track=track)
        flash("action recover successfully")
    else:
        flash("action not found")

    return redirect('/action')





