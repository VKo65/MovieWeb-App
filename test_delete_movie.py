from app import app
from datamanager.sqlite_data_manager import SQLiteDataManager

data_manager = SQLiteDataManager("instance/movies.db")

with app.app_context():
    movie_id = 1  # Einen existierenden Film zum Testen auswählen
    success = data_manager.delete_movie(movie_id)

    if success:
        print(f"✅ Film mit ID {movie_id} wurde erfolgreich gelöscht!")
    else:
        print(f"❌ Film mit ID {movie_id} nicht gefunden oder bereits gelöscht!")