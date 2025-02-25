from app import app
from datamanager.sqlite_data_manager import SQLiteDataManager

data_manager = SQLiteDataManager("instance/movies.db")

with app.app_context():  # ✅ Hier aktivieren wir den Application Context
    movie_id = 1  # ID des Films, der geändert werden soll
    new_data = {"title": "Inception - Director’s Cut", "rating": 9.0}

    if data_manager.update_movie(movie_id, new_data):
        print(f"✅ Film {movie_id} erfolgreich aktualisiert!")
    else:
        print(f"❌ Fehler beim Aktualisieren von Film {movie_id}.")