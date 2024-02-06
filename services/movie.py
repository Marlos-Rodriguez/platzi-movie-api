from models.movie import Movie
from sqlalchemy.orm.session import Session


class MovieService():
    def __init__(self, db: Session):
        self.db = db

    def get_movies(self) -> list[Movie]:
        return self.db.query(Movie).all()

    def get_movie_by_id(self, id: int) -> Movie:
        '''Get movie by ID'''
        return self.db.query(Movie).filter_by(id=id).first()

    def get_movie_by_category(self, category: str) -> list[Movie]:
        '''Get movie by Category'''
        return self.db.query(Movie).filter_by(category=category).all()

    def create_movie(self, new_movie: Movie) -> str:
        self.db.add(new_movie)
        self.db.commit()

        return "Movie Created"

    def modify_movie_by_id(self, id: int, new_movie: Movie) -> str:
        result = self.db.query(Movie).filter_by(id=id).first()
        if not result:
            return "Movie not found"

        result.category = new_movie.category
        result.overview = new_movie.overview
        result.rating = new_movie.rating
        result.title = new_movie.title
        result.year = new_movie.year

        self.db.commit()

        return "Movie modified"

    def delete_movie(self, id: int) -> str:
        result = self.db.query(Movie).filter_by(id=id).first()
        if not result:
            return "Movie not found"

        self.db.delete(result)
        self.db.commit()

        return "Movie Deleted"
