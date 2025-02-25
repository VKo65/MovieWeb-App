from datamanager.sqlite_data_manager import SQLiteDataManager

data_manager = SQLiteDataManager("instance/movies.db")

movie_title = "Inception"
movie_data = data_manager.fetch_movie_from_omdb(movie_title)

if movie_data:
    print(f"✅ Filmdaten für '{movie_title}': {movie_data}")
else:
    print("❌ Kein Film gefunden.")