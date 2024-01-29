from fastapi import Depends, FastAPI, HTTPException, Path, Query, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import List


from jwt_manager import create_token, validate_token
from config.database import session, engine, Base
from models.movie import Movie as MovieModel


app = FastAPI()
app.title = "My movie API"
app.version = "0.0.1"

db = session()

Base.metadata.create_all(bind=engine)


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Wrong credentials")


class User(BaseModel):
    email: str
    password: str


class Movie(BaseModel):
    id: int | None = None
    title: str = Field(min_length=5, max_length=15)
    overview: str | None = None
    year: int = Field(le=2023)
    rating: float = Field(ge=1, le=10)
    category: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 0,
                    "title": "Movie",
                    "overview": "Best movie ever",
                    "year": 2002,
                    "rating": 0.0,
                    "category": "Movie"
                }
            ]
        }
    }


movies: List[Movie] = [
    Movie(
        id=1,
        title="Avatar",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year=2009,
        rating=7.8,
        category="Accion"
    ),
    Movie(
        id=2,
        title="Avatarsss",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year=2009,
        rating=7.8,
        category="Accion"
    ),

    Movie(id=3,
          title="Avatarsss",
          overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
          year=2009,
          rating=7.8,
          category="Comedy")
]


@app.get("/movies", tags=['Movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    result = db.query(MovieModel).all()
    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)


@app.get("/movies/{id}", tags=["Movies"], response_model=Movie, responses={404: {"model": str}})
def get_movie_by_id(id: int = Path(ge=1, le=100)) -> Movie:
    '''Get movie by ID'''
    result = db.query(MovieModel).filter_by(id=id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)


@app.get("/movies/", tags=["Movies"], response_model=List[Movie])
def get_movie_by_category(category: str = Query(min_length=1)) -> List[Movie]:
    '''Get movie by Category'''
    result = db.query(MovieModel).filter_by(category=category).all()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)


@app.post("/movies", tags=["Movies"])
def create_movie(movie_request: Movie):
    new_movie = MovieModel(**movie_request.model_dump())
    db.add(new_movie)
    db.commit()

    return JSONResponse(status_code=201, content={"message": "Movie Created"})


@app.put("/movies/{id}", tags=["Movies"])
def modify_movie_by_id(id: int, new_movie: Movie):
    for i, item in enumerate(movies):
        if item.id == id:
            new_movie.id = id
            movies[i] = new_movie
    return JSONResponse(content={"message": "Movie modified"})


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    for item in movies:
        if item.id == id:
            movies.remove(item)
    return JSONResponse(content={"message": "Movie Deleted"})


@app.post("/login", tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content={"jwt": token})
