from flask import Flask
from mongoengine import connect
from routes.form import form_bp
from routes.action import action_bp
from routes.question import question_bp
from config import config
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)



app.register_blueprint(form_bp)
app.register_blueprint(action_bp)
app.register_blueprint(question_bp)


if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected DB")
    
    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'],
                debug=config['DEBUG'])
