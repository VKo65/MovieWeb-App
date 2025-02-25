from datamanager.sqlite_data_manager import SQLiteDataManager
from app import app  # App importieren, um den Kontext zu setzen

data_manager = SQLiteDataManager("instance/movies.db")

with app.app_context():  # <-- Anwendungskontext aktivieren
    new_user_id = data_manager.add_user("Charlie")

if new_user_id:
    print(f"✅ Neuer Benutzer {new_user_id} erfolgreich in der Datenbank!")
else:
    print("❌ Benutzer konnte nicht hinzugefügt werden!")