
from flask import Blueprint, request, jsonify, make_response
from extensions import db
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy.sql import func


following_bp = Blueprint('following_bp', __name__)

class Following(db.Model):
    __tablename__ = 'Follower_User'

    follower_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    followed_at = db.Column(db.DateTime, nullable=False, server_default=func.now())


    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, follower_id, followed_id, followed_at):
        self.follower_id = follower_id
        self.followed_id = followed_id
        self.followed_at = followed_at

    def __repr__(self):
        return f'<Following follower_id={self.follower_id}, followed_id={self.followed_id}>'

class FollowingSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Following
        sqla_session = db.session

    follower_id = fields.Integer(required=True)
    followed_id = fields.Integer(required=True)
    followed_at = fields.DateTime(required=True)


Following_schema = FollowingSchema()
Followings_schema = FollowingSchema(many=True)

@following_bp.route('/followings', methods=['GET'])
def get_followings():
    followings_list = Following.query.all()
    result = Followings_schema.dump(followings_list)
    return make_response(jsonify({"followings": result}), 200)


# curl -v http://127.0.0.1:5000/author/1
@following_bp.route('/following/<int:follower_id>/<int:followed_id>', methods=['GET'])
def get_following(follower_id, followed_id):
    following = Following.query.get((follower_id, followed_id))
    if following:
        result = Following_schema.dump(following)
        return jsonify(result), 200
    else:
        return jsonify({'message': 'Following relationship not found'}), 404



@following_bp.route('/followings', methods=['POST'])
def create_following():
    data = request.get_json()
    try:
        following_data = FollowingSchema().load(data)
        new_following = Following(**following_data)
        db.session.add(new_following)
        db.session.commit()
        return Following_schema.jsonify(new_following), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400



@following_bp.route('/following/<int:follower_id>/<int:followed_id>', methods = ['PUT'])
def update_following(follower_id, followed_id):
    following = Following.query.get((follower_id, followed_id))
    if following:
        data = request.get_json()
        following.follower_id = data.get('follower_id', following.follower_id)
        following.followed_id = data.get('followed_id', following.followed_id)
        following.followed_at = data.get('followed_at', following.followed_at)
        db.session.commit()
        return jsonify({'message': 'Following updated successfully'}), 200
    else:
        return jsonify({'message': 'Following not found'}), 404



@following_bp.route('/following/<int:follower_id>/<int:followed_id>', methods = ['DELETE'])
def delete_following(follower_id, followed_id):
    following = Following.query.get((follower_id, followed_id))
    if following:
        db.session.delete(following)
        db.session.commit()
        return jsonify({'message': 'Following deleted succesfully'}), 200
    else:
        return jsonify({'message': 'Following not found'}), 404
