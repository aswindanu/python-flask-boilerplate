import hashlib, datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from .model import Clients
from blueprints import db, app
from sqlalchemy import desc

from blueprints import internal_required
from flask_jwt_extended import jwt_required

#password Encription
from password_strength import PasswordPolicy

# 'client' penamaan (boleh diganti)
bp_client = Blueprint('client', __name__)
api = Api(bp_client)

class ClientResource(Resource):

    @jwt_required()
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()
        
        qry = Clients.query.get(args["id"])
        if qry is not None:
            return {"status":"success", "result":marshal(qry, Clients.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {'status':'failed', "result" : "ID Not Found"}, 404, {'Content-Type':'application/json'}

    def post(self):
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('username', location='json', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        validation = policy.test(args['password'])

        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()

            client = Clients(datetime.datetime.now(), args['username'], password_digest, 0)
            
            try:
                db.session.add(client)
                db.session.commit()
            except Exception as e:
                return {"status":"failed", "result": "Client Already Exist"}, 400, {'Content-Type':'application/json'}

            app.logger.debug('DEBUG : %s ', client )

            return {"status":"success", "result":marshal(client, Clients.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {"status":"failed", "result": "Wrong Password Length"}, 400, {'Content-Type':'application/json'}

    @jwt_required()
    def put(self):
        policy = PasswordPolicy.from_names(
            length=6
        )

        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        parser.add_argument('password', location='json', required=True)
        args = parser.parse_args()

        validation = policy.test(args['password'])

        qry = Clients.query.get(args["id"])

        if qry is None:
            return {'status':'failed',"result":"ID Not Found"}, 404, {'Content-Type':'application/json'}
        if validation == []:
            password_digest = hashlib.md5(args['password'].encode()).hexdigest()

            qry.password = password_digest
            db.session.commit()

            return {"status":"success", "result":marshal(qry, Clients.response_field)}, 200, {'Content-Type':'application/json'}
        
        return {"status":"failed", "result": "Wrong Password Length"}, 400, {'Content-Type':'application/json'}

    @jwt_required()
    @internal_required
    def delete(self):
        return {"status":"failed", "result":"Delete Not Available Now, Please Contact Developer"}, 403, {'Content-Type':'application/json'}
        
        parser = reqparse.RequestParser()
        parser.add_argument('id', location='args', required=True)
        args = parser.parse_args()

        qry = Clients.query.get(args["id"])
        if qry is None:
            return {'status':'failed',"result":"ID Not Found"}, 404, {'Content-Type':'application/json'}

        db.session.delete(qry)
        db.session.commit()

        return {"status":"success", "result":"Data with ID " + args["id"] + "Deleted"}, 200, {'Content-Type':'application/json'}

    def options(self):
        return {}, 200

class ClientList(Resource):

    def __init__(self):
        pass

    @jwt_required()
    @internal_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, location='args', default=1)
        parser.add_argument('per_page',type=int, location='args', default=25)
        parser.add_argument('status',location='args', type=inputs.boolean, help='invalid status', choices=(True,False))
        args =parser.parse_args()

        offset = (args['page'] * args['per_page']) - args['per_page']

        qry = Clients.query

        if args['status'] is not None:
            qry = qry.filter_by(status=args['status'])

        result = []
        for row in qry.limit(args['per_page']).offset(offset).all():
            result.append(marshal(row,Clients.response_field))
        
        return {"status":"success", "result":result}, 200, {'Content-Type':'application/json'}

    def options(self):
        return {}, 200



api.add_resource(ClientResource, '', '')
api.add_resource(ClientList,'','/list')