from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_required  
from melisa_orm.models.form import Form
from melisa_orm import Track,Validation
from melisa_orm.models.question import Question,QuestionKindEnum
from datetime import datetime
from flask_login import login_required 
question_bp = Blueprint('question', __name__)

@question_bp.route('/question')

def show_question():
    question = Question.objects()
    form= Form.objects(track__enable=True)
    return render_template('question.html', question=question,form=form,questionsenum=QuestionKindEnum)
@question_bp.route('/addquestion')
def addd_question():
    form= Form.objects(track__enable=True)
    return render_template('addquestion.html',form=form,questionsenum=QuestionKindEnum)

@question_bp.route('/question/add', methods=['POST'])
def add_question():

    form_data = request.form

    validation_names = form_data.getlist('validation_name[]')
    validation_exps = form_data.getlist('validation_exp[]')
    validation_error_msgs = form_data.getlist('validation_error_msg[]')
    if not validation_names:
        validation_names = ['']
    if not validation_exps:
        validation_exps = ['']
    if not validation_error_msgs:
        validation_error_msgs = ['']
    
    validations = [Validation(name=name, exp=exp, error_msg=error_msg) for name, exp, error_msg in zip(validation_names, validation_exps, validation_error_msgs)]

    question = Question(
        form=Form.objects.get(id=form_data['formu']),
        name=form_data['name'],
        description=form_data['description'],
        kind=QuestionKindEnum(form_data['kind']),
        order=int(form_data['order']),
        validations=validations,
        track=Track(user='user', created=datetime.now(), updated=datetime.now(), enable=True)  # Ajusta el usuario según tu lógica
    )

    question.save()

    flash("Question added successfully")
    return redirect('/question')
@question_bp.route('/editquestion/<string:question_id>', methods=['GET', 'POST'])
def edit_question(question_id):
    question = Question.objects(id=question_id).first()
    forms = Form.objects(track__enable=True)

    if request.method == 'POST':
        form_data = request.form

        validation_names = form_data.getlist('validation_name[]')
        validation_exps = form_data.getlist('validation_exp[]')
        validation_error_msgs = form_data.getlist('validation_error_msg[]')
        
        validations = [Validation(name=name, exp=exp, error_msg=error_msg) for name, exp, error_msg in zip(validation_names, validation_exps, validation_error_msgs)]

        question.update(
            form=Form.objects.get(id=form_data['formu']),
            name=form_data['name'],
            description=form_data['description'],
            kind=QuestionKindEnum(form_data['kind']),
            order=int(form_data['order']),
            validations=validations,
            track__user='user yo', 
            track__updated=datetime.now() 
        )



        flash("Question updated successfully")
        return redirect('/question')

    return render_template('edit_question.html', question=question, forms=forms, questionsenum=QuestionKindEnum)

@question_bp.route('/deletequestion/<string:question_id>')
def delete_question(question_id):
    question = Question.objects(id=question_id).first()

    if question:
        track = question.track

        track['enable'] = False
        track['user'] = 'deleted by yo'
        question.update(track=track)
        flash("question deleted successfully")
    else:
        flash("question not found")

    return redirect('/question')

@question_bp.route('/resetquestion/<string:question_id>')
def reset_question(question_id):
    question = Question.objects(id=question_id).first()

    if question:
        track = question.track

        track['enable'] = True
        track['user'] = 'recover by yo'
        question.update(track=track)
        flash("question recover successfully")
    else:
        flash("question not found")

    return redirect('/question')