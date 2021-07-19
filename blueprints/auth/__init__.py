from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
import json, hashlib
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt
from blueprints.client.model import Clients

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        password = hashlib.md5(args['password'].encode()).hexdigest()

        ###### from database #######
        qry = Clients.query

        qry = qry.filter_by(username = args['username'])
        qry = qry.filter_by(password = password).first()
         

        claim = marshal(qry, Clients.response_field)

        if qry is not None:
            token = create_access_token(identity=args['username'], user_claims=claim)
        else:
            return {'status':'failed', 'result': 'UNAUTHORIZED | invalid key or secret'}, 401

        return {"status":"success",'result': token}, 200, {'Content-Type':'application/json'}

    @jwt_required
    def get(self):
        claims = get_jwt()
        return {"status":"success", 'result': claims}, 200, {'Content-Type':'application/json'}

    def options(self):
        return {}, 200

api.add_resource(CreateTokenResource,'')
