from flask import Blueprint, request, jsonify, make_response
from extensions import db
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from marshmallow import fields
from marshmallow import validate
from include.collection import Collection
from include.artist import Artist 

song_bp = Blueprint('song_bp', __name__)

class Song(db.Model):
    __tablename__ = 'Song'

    song_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    collection_id = db.Column(db.Integer, db.ForeignKey('Collection.collection_id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    explicit = db.Column(db.Boolean, default=False)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, collection_id, title, duration, release_year, genre, explicit):
        self.collection_id = collection_id
        self.title = title
        self.duration = duration
        self.release_year = release_year
        self.genre = genre
        self.explicit = explicit

    def __repr__(self):
        return f'<Song {self.song_id}>'

class SongSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Song
        sqla_session = db.session

    song_id =  fields.Integer(dump_only=True)
    collection_id = fields.Integer(required=True)
    title = fields.String(required=True)
    duration = fields.Integer(required=True, validate=validate.Range(min=1))
    release_year = fields.Integer(required=True, validate=validate.Range(min=1950))
    genre =  fields.String(required=True)
    explicit = fields.Boolean(required=True)

song_schema = SongSchema()
songs_schema = SongSchema(many=True)

@song_bp.route('/songs', methods=['GET'])
def get_songs():
    songs_list = Song.query.all()
    result = songs_schema.dump(songs_list)
    return make_response(jsonify({"songs": result}), 200)


# curl -v http://127.0.0.1:5000/author/1
@song_bp.route('/song/<int:id>', methods = ['GET'])
def get_song(id):
    song = Song.query.get(id)
    if song:
        song_schema = SongSchema()
        song_json  = song_schema.dump(song)
        return jsonify(song_json), 200
    else:
        return jsonify({'message' : 'Song not found'}), 404
    

@song_bp.route('/songs', methods=['POST'])
def create_song():
    data = request.get_json()
    try:
        song_data = SongSchema().load(data)
        new_song = Song(**song_data)
        db.session.add(new_song)
        db.session.commit()
        return song_schema.jsonify(new_song), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

@song_bp.route('/song/<int:id>', methods = ['PUT'])
def update_song(id):
    song = Song.query.get(id)
    if song:
        data = request.get_json()
        song.collection_id = data.get('collection_id', song.collection_id)
        song.title = data.get('title', song.title)
        song.duration = data.get('duration', song.duration)
        song.release_year = data.get('release_year', song.release_year)
        song.genre = data.get('genre', song.genre)

        db.session.commit()
        return jsonify({'message': 'Song updated successfully'}), 200
    else:
        return jsonify({'message': 'Song not found'}), 404


@song_bp.route('/song/<int:id>', methods = ['DELETE'])
def delete_song(id):
    song = Song.query.get(id)
    if song:
        db.session.delete(song)
        db.session.commit()
        return jsonify({'message': 'Song deleted succesfully'}), 200
    else:
        return jsonify({'message': 'Song not found'}), 404
    
@song_bp.route('/songs/search', methods=['GET'])
def get_songs_title():
    title = request.args.get('title')

    query = (
        db.session.query(Song, Collection, Artist)
        .join(Collection, Song.collection_id == Collection.collection_id)
        .join(Artist, Collection.artist_id == Artist.artist_id)
    )

    if title:
        query = query.filter(Song.title.ilike(f"%{title}%"))

    results = query.all()

    response = []
    for song, collection, artist in results:
        response.append({
            "song_id": song.song_id,
            "title": song.title,
            "duration": song.duration,
            "release_year": song.release_year,
            "genre": song.genre,
            "explicit": song.explicit,
            "collection": {
                "collection_id": collection.collection_id,
                "title": collection.title,
                "type": collection.type,
                "release_date": collection.release_date.strftime('%Y-%m-%d'),
                "total_tracks": collection.total_tracks
            },
            "artist": {
                "artist_id": artist.artist_id,
                "name": artist.name,
            }
        })

    return make_response(jsonify(response), 200)

