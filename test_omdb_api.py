import requests

# OMDb API Key (achte darauf, dass dieser in einer .env Datei gespeichert wird)
API_KEY = "59fb2f5d"
BASE_URL = "http://www.omdbapi.com/"

def fetch_movie_from_omdb(title):
    """ Holt Filmdaten von der OMDb API für den vollen Titel """
    print(f"\n🔍 Anfrage für OMDb API mit Titel: {title}")

    params = {
        "t": title,  # Titel des Films
        "apikey": API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        # Falls die API keinen Film findet
        if data.get("Response") == "False":
            print(f"⚠️ Kein Film gefunden für: {title}")
            return None

        # Fehlerbehandlung für N/A-Werte
        rating_str = data.get("imdbRating", "N/A")
        try:
            rating = float(rating_str) if rating_str != "N/A" else None
        except ValueError:
            rating = None

        movie_data = {
            "title": data.get("Title"),
            "year": data.get("Year"),
            "director": data.get("Director"),
            "rating": rating
        }

        print(f"✅ Erfolgreich gefunden: {movie_data}")
        return movie_data

    except requests.exceptions.RequestException as e:
        print(f"❌ API-Anfrage fehlgeschlagen: {e}")
        return None

# 🔥 Testlauf mit verschiedenen Filmen
test_movies = [
    "Inception",
    "The Matrix",
    "Star Wars",
    "Interstellar",
    "Avatar",
    "Jurassic Park"
]

for movie in test_movies:
    fetch_movie_from_omdb(movie)