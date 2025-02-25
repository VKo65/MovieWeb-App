from models import db, User
from app import app

# Flask-App-Kontext setzen, damit SQLAlchemy funktioniert
with app.app_context():
    try:
        users = User.query.all()  # Alle User aus der Datenbank abrufen
        print("📋 Benutzer in der Datenbank:")
        for user in users:
            print(f"- {user.id}: {user.username}")
        if not users:
            print("⚠️ Keine Benutzer gefunden!")
    except Exception as e:
        print("❌ Fehler beim Abrufen der Benutzer:", e)