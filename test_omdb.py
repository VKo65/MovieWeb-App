import requests
from datamanager.sqlite_data_manager import SQLiteDataManager

data_manager = SQLiteDataManager("instance/movies.db")
movie_data = data_manager.fetch_movie_from_omdb("Interstellar")

API_KEY = "59fb2f5d"
BASE_URL = "http://www.omdbapi.com/"


def fetch_movie_details(title):
    """Holt Filmdetails von der OMDb API"""
    params = {
        "t": title,
        "apikey": API_KEY
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("Response") == "True":
            return {
                "title": data.get("Title"),
                "year": data.get("Year"),
                "director": data.get("Director"),
                "rating": data.get("imdbRating"),
                "plot": data.get("Plot"),
                "poster": data.get("Poster")
            }
        else:
            print(f"❌ Fehler: {data.get('Error')}")
            return None
    else:
        print(f"❌ HTTP Fehler: {response.status_code}")
        return None


# Testen mit "Inception"
if __name__ == "__main__":
    movie_title = "Inception"
    details = fetch_movie_details(movie_title)

    if details:
        print(f"🎬 **{details['title']}** ({details['year']})")
        print(f"🎭 Regie: {details['director']}")
        print(f"⭐ Bewertung: {details['rating']}")
        print(f"📖 Handlung: {details['plot']}")
        print(f"🖼️ Poster: {details['poster']}")
    else:
        print("⚠️ Keine Filmdaten gefunden.")

if movie_data:
    print("🎬 Gefundene Filmdaten:")
    print(movie_data)
else:
    print("⚠️ Kein Film gefunden.")