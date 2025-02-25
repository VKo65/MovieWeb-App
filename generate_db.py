"""from models import db
from flask import Flask
import os

# Flask App erstellen (nur für die DB-Generierung)
app = Flask(__name__)

# Absoluter Pfad für die Datenbank
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "instance", "movies.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Datenbank initialisieren
db.init_app(app)

# Datenbank & Tabellen erstellen
with app.app_context():
    db.create_all()
    print("✅ Datenbank wurde erfolgreich erstellt!")"""

from app import app  # 💡 Wichtig! Flask-App importieren
from models import db, User

def add_test_users():
    with app.app_context():  # Jetzt kennt Python 'app'
        if not User.query.first():  # Falls noch keine User existieren
            user1 = User(username="Alice")
            user2 = User(username="Bob")
            db.session.add_all([user1, user2])
            db.session.commit()
            print("✅ Testbenutzer wurden hinzugefügt!")
        else:
            print("⚠️ Testbenutzer existieren bereits!")

"""if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Stellt sicher, dass Tabellen existieren
        add_test_users()"""





def add_test_movies():
    """Fügt Testfilme in die Datenbank ein."""
    from models import Movie, db

    movie1 = Movie(title="Inception", director="Christopher Nolan", year=2010, rating=8.8, user_id=1)
    movie2 = Movie(title="The Matrix", director="Wachowski", year=1999, rating=8.7, user_id=1)
    movie3 = Movie(title="Interstellar", director="Christopher Nolan", year=2014, rating=8.6, user_id=2)

    db.session.add_all([movie1, movie2, movie3])
    db.session.commit()
    print("✅ Testfilme wurden hinzugefügt!")

if __name__ == "__main__":
    from app import app  # Stelle sicher, dass du die Flask-App importierst

    with app.app_context():  # App-Kontext aktivieren
        add_test_users()  # Falls nötig, fügt Benutzer hinzu
        add_test_movies()  # Diese Zeile stellt sicher, dass Filme eingefügt werden!