from flask import (
    Flask,
    request,
    json,
    current_app as apps,
)

## database import###
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

## JWT import
from flask_jwt_extended import (
    JWTManager,
    verify_jwt_in_request,
    get_jwt
)
from datetime import timedelta

# wrap
from functools import wraps

# CORS
from flask_cors import CORS

# Flask swagger UI
from flask_swagger_ui import get_swaggerui_blueprint

# Load ENV Python
import os
from dotenv import load_dotenv
load_dotenv()

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
from json import loads
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


app = Flask(__name__)
CORS(app)

DEBUG = loads(os.getenv("DEBUG").lower())
app.config['APP_DEBUG'] = DEBUG
app.config['PROPAGATE_EXCEPTIONS'] = DEBUG

#################
# JWT
###############

app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET")
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

jwt = JWTManager(app)
    
def internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims['status']:
            return {'status':'failed', 'message':'FORBIDDEN | Internal Only'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def non_internal_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['status']:
            return {'status':'failed', 'message':'FORBIDDEN | JWT NEEDED'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


####Database####


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(os.getenv("DATABASE_USER"), os.getenv("DATABASE_PASSWORD"), os.getenv("DATABASE_HOST"), os.getenv("DATABASE_PORT"),  os.getenv("DATABASE_NAME"))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
# DEPRECATED using Manager & MigrateCommand
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)  # command 'db' dapat menjalankan semua command MigrateCommand

###########Middleware#############
@app.after_request
def after_request(response):
    try:
        try:
            requestData = request.get_json()
        except Exception as e:
            requestData = request.args.to_dict()
        app.logger.warning("REQUEST_LOG\t%s", 
            json.dumps({
                'uri':request.full_path,
                'code':response.status,
                'method':request.method,
                'request':requestData,
                'response':json.loads(response.data.decode('utf-8'))}))
    except Exception:  # Pass for swagger UI
        pass
    return response

###############################
# Swagger UI
# See docs: 
# https://pypi.org/project/flask-swagger-ui/
# https://www.datascienceblog.net/post/programming/flask-api-development/
###############################

@app.route("/api/swagger.json")
def create_swagger_spec():
    filename = os.path.join(apps.root_path, '..', 'swagger.json')
    with open(filename) as test_file:
        data = json.load(test_file)
        return data

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/api/swagger.json'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Flask application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)

###############################
# Import blueprints
###############################

from blueprints.auth import bp_auth
from blueprints.client.resources import bp_client
from blueprints.pets.resources import bp_pets

# Swagger
app.register_blueprint(swaggerui_blueprint)

# App
app.register_blueprint(bp_auth, url_prefix='/login')
app.register_blueprint(bp_client, url_prefix='/client' )
app.register_blueprint(bp_pets, url_prefix='/pets' )

db.create_all()
