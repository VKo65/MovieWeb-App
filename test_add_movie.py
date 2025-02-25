from app import app  # Flask-App importieren
from datamanager.sqlite_data_manager import SQLiteDataManager

# Datenbankmanager initialisieren
data_manager = SQLiteDataManager("instance/movies.db")

# Test-Filmdaten
user_id = 1  # Wir fügen den Film für Benutzer mit ID 1 hinzu
title = "The Dark Knight"
director = "Christopher Nolan"
year = 2008
rating = 9.0

# Sicherstellen, dass die Datenbank innerhalb des Flask-App-Kontexts genutzt wird
with app.app_context():
    new_movie_id = data_manager.add_movie(user_id, title, director, year, rating)

    # Prüfen, ob der Film erfolgreich eingefügt wurde
    if new_movie_id:
        print(f"✅ Neuer Film mit ID {new_movie_id} wurde erfolgreich hinzugefügt!")
    else:
        print("❌ Film konnte nicht hinzugefügt werden!")