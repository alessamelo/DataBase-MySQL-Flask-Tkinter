from flask import Blueprint, request, jsonify, make_response
from extensions import db
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields


artist_bp = Blueprint('artist_bp', __name__)

class Artist(db.Model):
    __tablename__ = 'Artist'

    artist_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(200), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    active_since = db.Column(db.Integer, nullable=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, name, bio, country, active_since):
        self.name = name
        self.bio = bio
        self.country = country
        self.active_since = active_since
    
    def __repr__(self):
        return f'<Artist {self.artist_id}>'

class ArtistSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Artist
        sqla_session = db.session

    artist_id = fields.Integer(dump_only = True)
    name = fields.String(required=True)
    bio = fields.String(required=True)
    country = fields.String(required=True)
    active_since = fields.Integer(required=True)

artist_schema = ArtistSchema()
artists_schema = ArtistSchema(many=True)


@artist_bp.route('/artists', methods=['GET'])
def get_artists():
    artists_list = Artist.query.all()
    result = artists_schema.dump(artists_list)
    return make_response(jsonify({"artists": result}), 200)


@artist_bp.route('/artist/<int:id>', methods = ['GET'])
def get_artist(id):
    artist = Artist.query.get(id)
    if artist:
        artist_schema = ArtistSchema()
        artist_json  = artist_schema.dump(artist)
        return jsonify(artist_json), 200
    else:
        return jsonify({'message' : 'Artist not found'}), 404


@artist_bp.route('/artists', methods=['POST'])
def create_artist():
    data = request.get_json()
    try:
        artist_data = ArtistSchema().load(data)
        new_artist = Artist(**artist_data)
        db.session.add(new_artist)
        db.session.commit()
        return artist_schema.jsonify(new_artist), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@artist_bp.route('/artist/<int:id>', methods = ['PUT'])
def update_artist(id):
    artist = Artist.query.get(id)
    if artist:
        data = request.get_json()
        artist.name = data.get('name', artist.name)
        artist.bio = data.get('bio', artist.bio)
        artist.country = data.get('country', artist.country)
        artist.active_since = data.get('active_since', artist.active_since)
        
        db.session.commit()
        return jsonify({'message': 'Artist updated successfully'}), 200
    else:
        return jsonify({'message': 'Artist not found'}), 404


@artist_bp.route('/artist/<int:id>', methods = ['DELETE'])
def delete_artist(id):
    artist = Artist.query.get(id)
    if artist:
        db.session.delete(artist)
        db.session.commit()
        return jsonify({'message': 'Artist deleted succesfully'}), 200
    else:
        return jsonify({'message': 'Artist not found'}), 404


@artist_bp.route('/artists/songs', methods=['GET'])
def get_artist_songs():
    from include.song import Song
    from include.collection import Collection
    name = request.args.get('name')

    query = (
        db.session.query(Artist, Collection, Song)
        .join(Collection, Artist.artist_id == Collection.artist_id)
        .join(Song, Collection.collection_id == Song.collection_id)
    )

    if name:
        query = query.filter(Artist.name.ilike(f"%{name}%"))

    results = query.all()

    response = []
    for artist, collection, song in results:
        response.append({
            "artist": {
                "artist_id": artist.artist_id,
                "name": artist.name,
                "country": artist.country,
                "active_since": artist.active_since
            },
            "collection": {
                "collection_id": collection.collection_id,
                "title": collection.title,
                "type": collection.type,
                "release_date": collection.release_date.strftime('%Y-%m-%d'),
                "total_tracks": collection.total_tracks
            },
            "song": {
                "song_id": song.song_id,
                "title": song.title,
                "duration": song.duration,
                "release_year": song.release_year,
                "genre": song.genre,
                "explicit": song.explicit
            }
        })

    return make_response(jsonify(response), 200)


@artist_bp.route('/artist_login', methods=['POST'])
def login_artist_account():
    from include.user import User
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    artist_id = data.get("artist_id")

    if not username or not password or not artist_id:
        return jsonify({"error": "Se requieren username, password y artist_id"}), 400

    user = User.query.filter_by(username=username, password=password).first()

    if not user:
        return jsonify({"error": "Credenciales inválidas"}), 401

    if str(user.artist_id) != str(artist_id):
        return jsonify({"error": "El usuario no está vinculado al ID de artista indicado"}), 403

    return jsonify({
        "message": "Inicio de sesión de artista exitoso",
        "user_id": user.user_id,
        "artist_id": user.artist_id,
        "username": user.username
    }), 200

