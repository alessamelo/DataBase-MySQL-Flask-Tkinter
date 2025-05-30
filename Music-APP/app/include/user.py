# user.py
from flask import Blueprint, request, jsonify, make_response
from extensions import db
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from sqlalchemy.sql import func

user_bp = Blueprint('user_bp', __name__)

class User(db.Model):
    __tablename__ = 'User'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.artist_id'), nullable=True)
    username = db.Column(db.String(50), unique = True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    explicit_content = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    date_birth = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.Date, nullable=False, server_default=func.current_date()) 

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, username, first_name, last_name, password, email, date_birth, artist_id=None, explicit_content=False):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        self.date_birth = date_birth
        self.artist_id = artist_id
        self.explicit_content = explicit_content

    def __repr__(self):
        return f'<User {self.user_id}>'

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        sqla_session = db.session

    user_id = fields.Integer(dump_only=True)
    artist_id = fields.Integer(required=False, allow_none=True)
    username = fields.String(required=True)
    first_name = fields.String(required=True)
    last_name = fields.String(required=True)
    password = fields.String(required=True)
    explicit_content = fields.Boolean(required=False, load_default=False)
    email = fields.Email(required=True)
    date_birth = fields.Date(required=True)
    created_at = fields.Date(dump_only = True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users_list = User.query.all()
    result = users_schema.dump(users_list)
    return make_response(jsonify({"users": result}), 200)


# curl -v http://127.0.0.1:5000/author/1
@user_bp.route('/user/<int:id>', methods = ['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        user_schema = UserSchema()
        user_json  = user_schema.dump(user)
        return jsonify(user_json), 200
    else:
        return jsonify({'message' : 'User not found'}), 404
    

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    try:
        user_data = UserSchema().load(data)
        new_user = User(**user_data)
        db.session.add(new_user)
        db.session.commit()
        return user_schema.jsonify(new_user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@user_bp.route('/user/<int:id>', methods = ['PUT'])
def update_user(id):
    user = User.query.get(id)
    if user:
        data = request.get_json()
        user.artist_id = data.get('artist_id', user.artist_id)
        user.username = data.get('username', user.username)
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.password = data.get('password', user.password)
        user.explicit_content = data.get('explicit_content', user.explicit_content)
        user.email = data.get('email', user.email)
        user.date_birth = data.get('date_birth', user.date_birth)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404


@user_bp.route('/user/<int:id>', methods = ['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted succesfully'}), 200
    else:
        return jsonify({'message': 'User not found'}), 404



"""
curl -X POST http://127.0.0.1:5000/login \
     -H "Content-Type: application/json" \
     -d '{"username": "alguien", "password": "1234"}'
"""
@user_bp.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        return jsonify({
            "message": "Login successful",
            "user": user_schema.dump(user)
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401
