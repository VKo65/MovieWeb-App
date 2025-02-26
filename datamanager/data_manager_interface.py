from abc import ABC, abstractmethod

class DataManagerInterface(ABC):
    """A Interface for all DataManager-Classes."""

    @abstractmethod
    def get_all_users(self):
        """Get all users and give it back."""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass


    @abstractmethod
    def get_user_movies(self, user_id):

        pass

    @abstractmethod
    def add_user(self, username):

        pass

    @abstractmethod
    def add_movie(self, user_id, title, director, year, rating):

        pass

    @abstractmethod
    def update_movie(self, movie_id, title=None, director=None, year=None, rating=None):

        pass

    @abstractmethod
    def delete_movie(self, movie_id):

        pass