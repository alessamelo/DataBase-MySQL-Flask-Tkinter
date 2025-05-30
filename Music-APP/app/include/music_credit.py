from flask import Blueprint, request, jsonify, make_response
from extensions import db
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields

credit_bp = Blueprint('credit_bp', __name__)

class Credit(db.Model):
    __tablename__ = 'MusicCredit'
    
    music_credit_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('Song.song_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    role = db.Column(db.String(100), nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, song_id, user_id, role):
        self.song_id = song_id
        self.user_id = user_id
        self.role = role

    def __repr__(self):
        return f'<Credit song_id={self.song_id}, user_id={self.user_id}>'

class CreditSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Credit
        sqla_session = db.session

    music_credit_id = fields.Integer(dump_only=True)
    song_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    role = fields.String(required=True)

Credit_schema = CreditSchema()
Credits_schema = CreditSchema(many=True)

@credit_bp.route('/credits', methods=['GET'])
def get_credits():
    credits_list = Credit.query.all()
    result = Credits_schema.dump(credits_list)
    return make_response(jsonify({"Music_Credit": result}), 200)

@credit_bp.route('/credit/<int:credit_id>', methods=['GET'])
def get_credit(credit_id):
    credit = Credit.query.get(credit_id)
    if credit:
        result = Credit_schema.dump(credit)
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Credit relationship not found'}), 404

@credit_bp.route('/credits', methods=['POST'])
def create_credit():
    data = request.get_json()
    try:
        credit_data = Credit_schema.load(data)
        new_credit = Credit(**credit_data)
        db.session.add(new_credit)
        db.session.commit()
        return Credit_schema.jsonify(new_credit), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@credit_bp.route('/credit/<int:credit_id>', methods=['PUT'])
def update_credit(credit_id):
    credit = Credit.query.get(credit_id)
    if credit:
        data = request.get_json()
        credit.song_id = data.get('song_id', credit.song_id)
        credit.user_id = data.get('user_id', credit.user_id)
        credit.role = data.get('role', credit.role)
        db.session.commit()
        return jsonify({'message': 'Credit updated successfully'}), 200
    else:
        return jsonify({'message': 'Credit not found'}), 404

@credit_bp.route('/credit/<int:credit_id>', methods=['DELETE'])
def delete_credit(credit_id):
    credit = Credit.query.get(credit_id)
    if credit:
        db.session.delete(credit)
        db.session.commit()
        return jsonify({'message': 'Song Credit deleted successfully'}), 200
    else:
        return jsonify({'message': 'Song Credit not found'}), 404
