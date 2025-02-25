from app import app
from datamanager.sqlite_data_manager import SQLiteDataManager

data_manager = SQLiteDataManager("instance/movies.db")

with app.app_context():
    user_id = 1  # Testen mit Alice (id = 1)
    movies = data_manager.get_user_movies(user_id)

    print(f"🎬 Filme von Benutzer {user_id}:")
    for movie in movies:
        print(f"- {movie.title} ({movie.year}), Regie: {movie.director}, Bewertung: {movie.rating}")
    if not movies:
        print("⚠️ Keine Filme gefunden!")