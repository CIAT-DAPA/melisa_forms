from flask import Blueprint, render_template, redirect, request, flash
from flask_login import login_user, logout_user, current_user
from models.models import User
from aclimate_orm import Users

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.get(username)

        if user and user.check_password(password):
            
            if user.is_admin():
                login_user(user)
                flash('Logged in as admin', 'success')
                return redirect('/form')
            else:
                flash('User is not an admin', 'error')
        else:
            flash('Incorrect credentials', 'error')

    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out', 'success')
    return redirect('/login')
