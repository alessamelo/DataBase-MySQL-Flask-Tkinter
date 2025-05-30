from flask import Flask
from extensions import db  # Importación directa
from include.artist import artist_bp
from include.user import user_bp
from include.collection import collection_bp
from include.following import following_bp
from include.song import song_bp
from include.music_credit import credit_bp
from include.streaming import streaming_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:minimi@localhost:3306/PROYECT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización
db.init_app(app)

# Blueprints (con prefijo API)
app.register_blueprint(artist_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(collection_bp, url_prefix='/api')
app.register_blueprint(following_bp, url_prefix='/api')
app.register_blueprint(song_bp, url_prefix='/api')
app.register_blueprint(credit_bp, url_prefix='/api')
app.register_blueprint(streaming_bp, url_prefix='/api')
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)