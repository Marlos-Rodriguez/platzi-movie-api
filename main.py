from fastapi import FastAPI
# from fastapi.responses import HTMLResponse
from pydantic import BaseModel


app = FastAPI()
app.title = "My movie API"
app.version = "0.0.1"


class Movie(BaseModel):
    id: int | None = None
    title: str
    overview: str | None = None
    year: int
    rating: float | None = None
    category: str


movies: list[Movie] = [
    Movie(
        id=1,
        title="Avatar",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year="2009",
        rating=7.8,
        category="Accion"
    ),
    Movie(
        id=2,
        title="Avatarsss",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year="2009",
        rating=7.8,
        category="Accion"
    ),

    Movie(id=3,
          title="Avatarsss",
          overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
          year="2009",
          rating=7.8,
          category="Comedy")
]


@app.get("/movies", tags=['Movies'])
def get_movies():
    return movies


@app.get("/movies/{id}", tags=["Movies"])
def get_movie_by_id(id: int):
    '''Get movie by ID'''
    return next((movie for movie in movies if movie.id == id), [])


@app.get("/movies/", tags=["Movies"])
def get_movie_by_category(category: str):
    '''Get movie by Category'''
    return [movie for movie in movies if movie.category == category]


@app.post("/movies", tags=["Movies"])
def create_movie(new_movie: Movie):
    new_movie.id = len(movies) + 1
    movies.append(new_movie)
    return movies


@app.put("/movies/{id}", tags=["Movies"])
def modify_movie_by_id(id: int, new_movie: Movie):
    for i, item in enumerate(movies):
        if item.id == id:
            new_movie.id = id
            movies[i] = new_movie
    return movies
