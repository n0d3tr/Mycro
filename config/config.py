from flask import Flask,session
from flask_restful import Api, Resource
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask.logging import default_handler
import gunicorn  
import psycopg2
import configparser
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import os
from logging.config import dictConfig

class bcolors: 
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

config = configparser.ConfigParser()
config.read('.env')
configurate = config['CONFIGURATION']


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__,template_folder=os.getcwd()+'/resource/view/',static_folder=os.getcwd()+'/public/',static_url_path='')
app.logger.removeHandler(default_handler)

if configurate.get('APP_DEBUG') == 'false':
    app_debug = False
elif configurate.get('APP_DEBUG') == 'true':
    app_debug = True
app.debug = app_debug

app.config['SECRET_KEY'] = configurate.get('APP_KEY')
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://'+configurate.get('DB_USERNAME')+':'+configurate.get('DB_PASSWORD')+'@'+configurate.get('DB_HOST')+'/'+configurate.get('DB_DATABASE') 
 
db = SQLAlchemy(app)
db.init_app(app)

bcrypt = Bcrypt(app)
api = Api(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*","headers":"X-Custom-Header"}})


