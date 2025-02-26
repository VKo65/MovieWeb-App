import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from models import db  # Importiere db aus models.py
from datamanager.sqlite_data_manager import SQLiteDataManager
import logging
import requests

app = Flask(__name__)

API_KEY = os.getenv("OMDB_API_KEY")

# Absoluter Pfad für SQLAlchemy setzen
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "movies.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Logging einrichten
logging.basicConfig(filename='error.log', level=logging.ERROR)

# SQLiteDataManager mit dem fixen Pfad initialisieren
data_manager = SQLiteDataManager("instance/movies.db")



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/users')
def list_users():
    users = data_manager.get_all_users()

    return render_template('users.html', users=users)


@app.route('/movies/<int:user_id>')
def user_movies(user_id):
    user = data_manager.get_user_by_id(user_id)  # Holt den Benutzer
    movies = data_manager.get_user_movies(user_id)  # Holt die Filme

    if not user:
        return "❌ Benutzer nicht gefunden!", 404

    return render_template("movies.html", user=user, movies=movies)


@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    """Löscht einen Film und leitet den Benutzer zurück zur Filmseite."""
    success = data_manager.delete_movie(movie_id)

    if success:
        print(f"✅ Film mit ID {movie_id} wurde gelöscht.")
    else:
        print(f"❌ Film mit ID {movie_id} nicht gefunden.")

    return redirect(request.referrer or url_for('home'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            data_manager.add_user(username)
            return redirect(url_for('list_users'))  # Leitet zur Benutzerliste weiter

    return render_template('add_user.html')  # Zeigt das Formular


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):


    user = data_manager.get_user_by_id(user_id)

    if not user:
        return "❌ Benutzer nicht gefunden!", 404

    if request.method == 'POST':
        title = request.form['title']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']

        movie_id = data_manager.add_movie(user_id, title, director, year, rating)
        if movie_id:
            return redirect(f"/movies/{user_id}")

    return render_template("add_movie.html", user=user)


@app.route('/movies/<int:movie_id>/edit', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = data_manager.get_movie_by_id(movie_id)  # Holt den Film
    if not movie:
        return "❌ Film nicht gefunden!", 404

    if request.method == 'POST':
        # Formulardaten auslesen
        title = request.form['title']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']

        # Aktualisierte Daten in ein Dictionary packen
        new_data = {
            "title": title,
            "director": director,
            "year": int(year),
            "rating": float(rating)
        }

        # Update-Funktion ausführen
        success = data_manager.update_movie(movie_id, new_data)
        if success:
            return redirect(url_for('user_movies', user_id=movie.user_id))
        else:
            return "❌ Fehler beim Aktualisieren!", 500

    return render_template('edit_movie.html', movie=movie)


@app.route('/fetch_movie_data')
def fetch_movie_data():
    title = request.args.get("title")

    if not title:
        return jsonify({"success": False, "error": "Kein Titel angegeben"}), 400

    url = f"http://www.omdbapi.com/?t={title}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["Response"] == "True":
        return jsonify({
            "success": True,
            "director": data.get("Director", "Unbekannt"),
            "year": data.get("Year", "N/A"),
            "rating": data.get("imdbRating", "N/A"),
        })
    else:
        return jsonify({"success": False, "error": "Film nicht gefunden"}), 404



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"🚨 Server Error: {e}")
    return render_template('500.html'), 500


if __name__ == '__main__':

    app.run(debug=True)