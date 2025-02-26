from models import db, User, Movie

class DataManager:
    """ Class to manage DB action"""

    @staticmethod
    def get_users():
        """Gives all user. """
        return User.query.all()

    @staticmethod
    def get_movies(user_id=None):
        """Gives all movies. If a user id available, only for this user """
        if user_id:
            return Movie.query.filter_by(user_id=user_id).all()
        return Movie.query.all()

    @staticmethod
    def add_movie(title, director, year, rating, user_id):
        """Add Movie to DB"""
        new_movie = Movie(title=title, director=director, year=year, rating=rating, user_id=user_id)
        db.session.add(new_movie)
        db.session.commit()
        return new_movie

    @staticmethod
    def update_movie(movie_id, title=None, director=None, year=None, rating=None):
        """Update a movie"""
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
        """Delete a movie from DB"""
        movie = Movie.query.get(movie_id)
        if movie:
            db.session.delete(movie)
            db.session.commit()
            return True
        return False