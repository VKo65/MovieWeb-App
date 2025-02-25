from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """Ein Interface für alle zukünftigen DataManager-Klassen."""

    @abstractmethod
    def get_all_users(self):
        """Gibt alle Benutzer zurück."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass


    @abstractmethod
    def get_user_movies(self, user_id):
        """Gibt alle Filme eines bestimmten Benutzers zurück."""
        pass

    @abstractmethod
    def add_user(self, username):
        """Fügt einen neuen Benutzer hinzu."""
        pass

    @abstractmethod
    def add_movie(self, user_id, title, director, year, rating):
        """Fügt einen neuen Film hinzu."""
        pass

    @abstractmethod
    def update_movie(self, movie_id, title=None, director=None, year=None, rating=None):
        """Aktualisiert einen Film."""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Löscht einen Film."""
        pass