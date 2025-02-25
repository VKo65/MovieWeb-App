import os
from dotenv import load_dotenv
from models import db, User, Movie
from flask_sqlalchemy import SQLAlchemy
from datamanager.data_manager_interface import DataManagerInterface
import requests

load_dotenv()
OMDB_API_KEY = os.getenv("OMDB_API_KEY")

class SQLiteDataManager(DataManagerInterface):
    """DataManager für SQLite, der das Interface implementiert."""

    def __init__(self, db_file_name):

        self.db = db  # ✅ Nutzt die bestehende Flask-Datenbankverbindung
        self.db_file_name = db_file_name

    def get_all_users(self):
        """Gibt alle Benutzer zurück.✅"""
        return User.query.all()

    def get_user_by_id(self, user_id):
        """Gibt den Benutzer mit der angegebenen ID zurück, mit Fehlerhandling"""
        try:
            return self.db.session.get(User, user_id)  # Holt den User anhand der ID
        except Exception as e:
            print(f"❌ Fehler beim Abrufen des Benutzers: {e}")
            return None


    def get_user_movies(self, user_id):
        """Gibt alle Filme eines bestimmten Benutzers zurück.
        filter_by(user_id=user_id) sucht alle Filme des entsprechenden Users.
        all gibt dann eine Liste zurück
        Laüft noch nicht❌"""
        return Movie.query.filter_by(user_id=user_id).all()


    def add_user(self, username):
        """Fügt einen neuen Benutzer zur Datenbank hinzu."""
        try:
            new_user = User(username=username)
            self.db.session.add(new_user)
            self.db.session.commit()
            print(f"✅ Benutzer {username} mit ID {new_user.id} hinzugefügt.")
            return new_user.id
        except Exception as e:
            print(f"❌ Fehler beim Hinzufügen des Benutzers {username}: {e}")
            self.db.session.rollback()
            return None

    def add_movie(self, user_id, title, director, year, rating):
        """Fügt einen neuen Film zur Datenbank hinzu."""
        new_movie = Movie(title=title, director=director, year=year, rating=rating, user_id=user_id)

        try:
            self.db.session.add(new_movie)
            self.db.session.commit()
            return new_movie.id
        except Exception as e:
            self.db.session.rollback()
            print(f"❌ Fehler beim Hinzufügen des Films: {e}")
            return None

    def update_movie(self, movie_id, new_data):
        """Aktualisiert einen vorhandenen Film mit neuen Daten."""
        movie = self.db.session.get(Movie, movie_id)  # Film suchen

        if movie:
            for key, value in new_data.items():
                setattr(movie, key, value)  # Neue Werte setzen

            self.db.session.commit()  # Änderungen speichern
            return True
        else:
            return False


    def get_movie_by_id(self, movie_id):
        """Gibt einen Film anhand der ID zurück."""
        return self.db.session.get(Movie, movie_id)


    def delete_movie(self, movie_id):
        """Löscht einen Film."""
        movie = Movie.query.get(movie_id)
        if movie:
            self.db.session.delete(movie)
            self.db.session.commit()
            return True
        return False


    def fetch_movie_from_omdb(self, title):
        """Holt Filminformationen aus der OMDb API."""
        url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"

        try:
            response = requests.get(url)
            data = response.json()

            if data["Response"] == "True":
                return {
                    "title": data["Title"],
                    "director": data["Director"],
                    "year": int(data["Year"]),
                    "rating": float(data["imdbRating"]),
                }
            else:
                print(f"⚠️ Kein Film gefunden für: {title}")
                return None
        except Exception as e:
            print(f"❌ Fehler beim Abrufen der Filmdaten: {e}")
            return None
