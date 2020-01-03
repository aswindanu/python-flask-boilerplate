from blueprints import db
from flask_restful import fields


class Pets(db.Model):
    __tablename__ = "pets"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    pet_name = db.Column(db.String(100), nullable=False)
    pet_type = db.Column(db.String(100), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    response_field = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'pet_name': fields.String,
        'pet_type': fields.String,
        'client_id': fields.Integer,
    }

    response_field_with_client = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'pet_name': fields.String,
        'pet_type': fields.String,
        'client_id': fields.Integer,
        'username': fields.String,
        'status': fields.Boolean,
    }

    response_field_organisasi = {
        'page': fields.Integer,
        'total_page': fields.Integer,
        'per_page': fields.Integer    
    }

    def __init__(self, created_at, pet_name, pet_type, client_id):
        self.created_at = created_at
        self.pet_name = pet_name
        self.pet_type = pet_type
        self.client_id = client_id

    def __repr__(self):
        return '<Pets %r>' % self.id