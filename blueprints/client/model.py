from blueprints import db
from flask_restful import fields


class Clients(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean, nullable=True, default=False)
    
    response_field = {
        'id': fields.Integer,
        'created_at': fields.DateTime,
        'username': fields.String,
        'status': fields.Boolean,
        # True if internal
    }

    def __init__(self,created_at, username,password, status):
        self.created_at = created_at
        self.username = username
        self.password = password
        self.status = status

    def __repr__(self):
        return '<Client %r>' % self.id