from flask import Blueprint, request, jsonify, make_response
from extensions import db
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy.sql import func

streaming_bp = Blueprint('streaming_bp', __name__)

class Streaming(db.Model):
    __tablename__ = 'StreamingDetails'

    streaming_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.song_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, user_id, song_id):
        self.user_id = user_id
        self.song_id = song_id

    def __repr__(self):
        return f"<Streaming {self.streaming_id}>"

class StreamingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Streaming
        sqla_session = db.session

    streaming_id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    song_id = fields.Integer(required=True)
    date = fields.DateTime(dump_only=True)

streaming_schema = StreamingSchema()
streamings_schema = StreamingSchema(many=True)

@streaming_bp.route('/streamings', methods=['GET'])
def get_streamings():
    streamings = Streaming.query.all()
    result = streamings_schema.dump(streamings)
    return make_response(jsonify(result), 200)

@streaming_bp.route('/streamings', methods=['POST'])
def create_streaming():
    data = request.get_json()
    try:
        streaming_data = streaming_schema.load(data)
        new_streaming = Streaming(
            user_id=streaming_data['user_id'],
            song_id=streaming_data['song_id']
        )
        db.session.add(new_streaming)
        db.session.commit()
        return streaming_schema.jsonify(new_streaming), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@streaming_bp.route('/streamings/<int:id>', methods=['DELETE'])
def delete_streaming(id):
    streaming = Streaming.query.get(id)
    if streaming:
        db.session.delete(streaming)
        db.session.commit()
        return jsonify({'message': 'Streaming deleted successfully'}), 200
    else:
        return jsonify({'message': 'Streaming not found'}), 404