import datetime
from flask import Blueprint
from flask_restful import Resource, Api, reqparse, marshal, inputs

from blueprints import internal_required, non_internal_required
from flask_jwt_extended import jwt_required, get_jwt

from .model import Pets
from blueprints.client.model import Clients

from blueprints import db, app
from sqlalchemy import desc

bp_pets = Blueprint("Pets", __name__)
api = Api(bp_pets)


class PetsResource(Resource):

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id',location='args', help='invalid id', required=True)
        args = parser.parse_args()

        qry = Pets.query.get(args["id"])

        if qry is not None:
            return {"status":"success", "result":marshal(qry, Pets.response_field)}, 200, {'Content-Type':'application/json'}

        return {'status':'failed',"result":"ID Not Found"}, 404, {'Content-Type':'application/json'}


    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("pet_name",location="json", help="invalid pet_name", required=True)
        parser.add_argument("pet_type",location="json", help="invalid pet_type", required=True)
        args = parser.parse_args()
        
        claims = get_jwt()

        qry = Pets(datetime.datetime.now(), args["pet_name"], args["pet_type"],claims["id"])

        db.session.add(qry)
        db.session.commit()

        app.logger.debug("DEBUG : %s ", qry)

        return {"status":"success", "result":marshal(qry, Pets.response_field)}, 200, {"Content-Type":"application/json"}

    @jwt_required()
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument("id",location="args", help="invalid id", required=True)

        parser.add_argument("pet_name",location="json", help="invalid pet_name", required=True)
        parser.add_argument("pet_type",location="json", help="invalid pet_type", required=True)
        args = parser.parse_args()

        qry = Pets.query.get(args["id"])

        if qry is None:
            return {"status":"failed","result":"ID Not Found"}, 404, {"Content-Type":"application/json"}

        qry.pet_name = args["pet_name"]
        qry.pet_type = args["pet_type"]
        db.session.commit()

        return {"status":"success", "result":marshal(qry, Pets.response_field)}, 200, {"Content-Type":"application/json"}

    
    @jwt_required()
    @internal_required
    def delete(self):
        return {"status":"failed", "result":"Delete Not Available Now, Please Contact Developer"}, 403, {"Content-Type":"application/json"}
        
        parser = reqparse.RequestParser()
        parser.add_argument("id",location="json", help="invalid id", required=True)
        args = parser.parse_args()

        qry = Pets.query.get(args["id"])

        if qry is None:
            return {"status":"failed","result":"ID Not Found"}, 404, {"Content-Type":"application/json"}

        db.session.delete(qry)
        db.session.commit()

        return {"status":"success", "result":marshal(qry, Pets.response_field)}, 200, {"Content-Type":"application/json"}

    def options(self):
        return {}, 200

class PetsResourceList(Resource):

    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("p", type=int, location="args", default=1)
        parser.add_argument("rp",type=int, location="args", default=25)
        parser.add_argument("id",type=int,location="args", help="invalid pets id")
        parser.add_argument("pet_name",location="args", help="invalid isbn")
        parser.add_argument("pet_type",location="args", help="invalid isbn")
        args =parser.parse_args()

        offset = (args["p"] * args["rp"]) - args["rp"]

        qry = Pets.query

        if args["id"] is not None:
            qry = qry.filter_by(id=args["id"])

        if args["pet_name"] is not None:
            qry = qry.filter_by(pet_name=args["pet_name"])

        if args["pet_type"] is not None:
            qry = qry.filter_by(pet_type=args["pet_type"])

        result = []
        for row in qry.limit(args["rp"]).offset(offset).all():
            result.append(marshal(row, Pets.response_field))
        
        results = {}
        results["page"] = args["p"]
        results["total_page"] = len(result) // args["rp"] +1
        results["per_page"] = args["rp"]
        results["data"] = result
        
        return {"status":"success", "result":results}, 200, {"Content-Type":"application/json"}

    def options(self):
        return {}, 200

class PetsWithClient(Resource):

    @jwt_required()
    def get(self):
        qry = db.session.query(Pets, Clients).join(Pets, Pets.client_id == Clients.id).all()
        
        result = []
        for data in qry:
            holder = marshal(data[0], Pets.response_field_with_client)
            holder["username"] = data[1].username
            holder["status"] = data[1].status
            result.append(holder)

        if qry is not None:
            return {"status":"success", "result":result}, 200, {"Content-Type":"application/json"}

        return {"status":"failed","result":"ID Not Found"}, 404, {"Content-Type":"application/json"}

    def options(self):
        return {}, 200

api.add_resource(PetsResource, "","")
api.add_resource(PetsResourceList, "/list")
api.add_resource(PetsWithClient, "/list/customer")

