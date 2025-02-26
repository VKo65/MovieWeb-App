import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
from models import db  # Importiere db aus models.py
from datamanager.sqlite_data_manager import SQLiteDataManager
import logging
import requests

app = Flask(__name__)

API_KEY = os.getenv("OMDB_API_KEY")

# Set absolute path to SQLAlchemy
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "instance", "movies.db")

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Logging
logging.basicConfig(filename='error.log', level=logging.ERROR)

# Initialise SQLiteDataManager with fixe path
data_manager = SQLiteDataManager("instance/movies.db")



@app.route('/')
def home():
    """Homepage Route - Displays the main welcome page."""
    return render_template('home.html')

@app.route('/users')
def list_users():
    """Displays a list of all registered users."""
    users = data_manager.get_all_users()

    return render_template('users.html', users=users)


@app.route('/movies/<int:user_id>')
def user_movies(user_id):
    """
        Displays all movies for a specific user.
        Args:
            user_id (int): The ID of the user.
        Returns:
            Rendered HTML page with the list of movies for user.
        """
    user = data_manager.get_user_by_id(user_id)
    movies = data_manager.get_user_movies(user_id)

    if not user:
        return "❌ Benutzer nicht gefunden!", 404

    return render_template("movies.html", user=user, movies=movies)


@app.route('/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(movie_id):
    """
    Deletes one specific movie from the database.
    Args:
        movie_id (int): The ID of the movie.
    Returns:
        Redirects to the user's movie list after successful deletion.
    """
    success = data_manager.delete_movie(movie_id)

    if success:
        print(f"✅ Film mit ID {movie_id} wurde gelöscht.")
    else:
        print(f"❌ Film mit ID {movie_id} nicht gefunden.")

    return redirect(request.referrer or url_for('home'))


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """
        Handles the addition of a new user.
        - If GET request: Displays the user registration form.
        - If POST request: Processes the form and adds a new user to the database.
        Returns:
            Redirects to the user list upon success or renders the form again if failed.
        """
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            data_manager.add_user(username)
            return redirect(url_for('list_users'))

    return render_template('add_user.html')


@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
        Allows users to add a new movie.
        - If GET request: Displays the movie addition form.
        - If POST request: Processes the form and saves the movie in the database.
        Args:
            user_id (int): The ID of the user adding the movie.
        Returns:
            Redirects to the user's movie list upon success.
        """

    user = data_manager.get_user_by_id(user_id)

    if not user:
        return "❌ User not found!", 404

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
    """
        Allows users to update the details of a movie.
        - If GET request: Displays the edit form with current movie data.
        - If POST request: Updates the movie information in database.
        Args:
            movie_id (int): The ID of the movie.
        Returns:
            Redirects to the user's movie list after a successful update.
        """
    movie = data_manager.get_movie_by_id(movie_id)
    if not movie:
        return "❌ Movie not found!", 404

    if request.method == 'POST':

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
    """
        Fetches movie details from the OMDb API based on a given title.
        This function is called via JavaScript when the user enters a movie title.
        It queries the OMDb API and returns relevant movie details in JSON-format.
        Returns:
            JSON response containing movie details if found.
        """
    title = request.args.get("title")

    if not title:
        return jsonify({"success": False, "error": "No input of title"}), 400

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
        return jsonify({"success": False, "error": "Movie not found"}), 404



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    logging.error(f"🚨 Server Error: {e}")
    return render_template('500.html'), 500


if __name__ == '__main__':

    app.run(debug=True)