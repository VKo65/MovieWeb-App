from models import db, User, Movie

class DataManager:
    """ Klasse zur Verwaltung der Datenbank-Interaktionen. """

    @staticmethod
    def get_users():
        """ Gibt alle Benutzer zurück. """
        return User.query.all()

    @staticmethod
    def get_movies(user_id=None):
        """ Gibt alle Filme zurück. Falls eine user_id übergeben wird, nur die Filme des Nutzers. """
        if user_id:
            return Movie.query.filter_by(user_id=user_id).all()
        return Movie.query.all()

    @staticmethod
    def add_movie(title, director, year, rating, user_id):
        """ Fügt einen neuen Film zur Datenbank hinzu. """
        new_movie = Movie(title=title, director=director, year=year, rating=rating, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    @staticmethod
    def update_movie(movie_id, title=None, director=None, year=None, rating=None):
        """ Aktualisiert einen bestehenden Film. """
        movie = Movie.query.get(movie_id)
        if not movie:
            return None

        if title:
            movie.title = title
        if director:
            movie.director = director
        if year:
            movie.year = year
        if rating:
            movie.rating = rating

        db.session.commit()
        return movie

    @staticmethod
    def delete_movie(movie_id):
        """ Löscht einen Film aus der Datenbank. """
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False