from flask import Blueprint, request, jsonify, make_response
from extensions import db
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy.types import Enum
from marshmallow import validate

collection_bp = Blueprint('collection_bp', __name__)

class Collection(db.Model):
    __tablename__ = 'Collection'

    collection_id = db.Column(db.Integer, primary_key=True, autoincrement =True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(Enum('Album', 'EP', 'Single', name='collection_type'), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    total_tracks = db.Column(db.Integer, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.artist_id'), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, title, type, release_date, total_tracks, artist_id):
        self.title = title
        self.type = type
        self.release_date = release_date
        self.total_tracks = total_tracks
        self.artist_id = artist_id
    
    def __repr__(self):
        return f'<Collection {self.collection_id}>'

class CollectionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Collection
        sqla_session = db.session

    collection_id = fields.Integer(dump_only=True)
    title = fields.String(required = True)
    type = fields.String(required=True, validate=validate.OneOf(['Album', 'EP', 'Single']))
    release_date = fields.Date(required = True)
    total_tracks = fields.Integer( required =True)
    artist_id = fields.Integer( required =True)

collection_schema = CollectionSchema()
collections_schema = CollectionSchema(many=True)


@collection_bp.route('/collections', methods=['GET'])
def get_collections():
    collections_list = Collection.query.all()
    result = collections_schema.dump(collections_list)
    return make_response(jsonify({"collections": result}), 200)


@collection_bp.route('/collection/<int:id>', methods = ['GET'])
def get_collection(id):
    collection = Collection.query.get(id)
    if collection:
        collection_schema = CollectionSchema()
        collection_json  = collection_schema.dump(collection)
        return jsonify(collection_json), 200
    else:
        return jsonify({'message' : 'Collection not found'}), 404


@collection_bp.route('/collections', methods=['POST'])
def create_collection():
    data = request.get_json()
    try:
        collection_data = CollectionSchema().load(data)
        new_collection = Collection(**collection_data)
        db.session.add(new_collection)
        db.session.commit()
        return collection_schema.jsonify(new_collection), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@collection_bp.route('/collection/<int:id>', methods = ['PUT'])
def update_collection(id):
    collection = Collection.query.get(id)
    if collection:
        data = request.get_json()

        collection.title = data.get('title', collection.title)
        collection.type = data.get('type', collection.type)
        collection.release_date = data.get('release_date', collection.release_date)
        collection.total_tracks = data.get('total_tracks', collection.total_tracks)
        collection.artist_id = data.get('artist_id', collection.artist_id)
        
        db.session.commit()
        return jsonify({'message': 'Collection updated successfully'}), 200
    else:
        return jsonify({'message': 'Collection not found'}), 404


@collection_bp.route('/collection/<int:id>', methods = ['DELETE'])
def delete_collection(id):
    collection = Collection.query.get(id)
    if collection:
        db.session.delete(collection)
        db.session.commit()
        return jsonify({'message': 'Collection deleted succesfully'}), 200
    else:
        return jsonify({'message': 'Collection not found'}), 404

