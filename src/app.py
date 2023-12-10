from flask import Flask
from mongoengine import connect
from routes.form import form_bp
from routes.action import action_bp
from routes.question import question_bp
from routes.melisa import melisa_bp
from routes.login import login_bp
from models.models import User
from config import config
import os
import flask_login

app = Flask(__name__)
app.secret_key = os.urandom(24)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Configuración del login manager
@login_manager.user_loader
def load_user(email):
    return User.get(email) 

connect(host=config['CONNECTION_DB'], alias='default')
connect(host=config['CONNECTION_DB2'], alias='db2')

app.register_blueprint(form_bp)
app.register_blueprint(action_bp)
app.register_blueprint(question_bp)
app.register_blueprint(melisa_bp)
app.register_blueprint(login_bp)


if __name__ == '__main__':

    print("Connected DB")
    print("Connected DB2")
    
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'],
                debug=config['DEBUG'])
