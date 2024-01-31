from typing import List
from fastapi import Depends, FastAPI, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


from jwt_manager import create_token
from config.database import session, engine, Base
from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie as MovieModel
from middlewares.error_handler import ErrorHandler


app = FastAPI()
app.title = "My movie API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

db = session()

Base.metadata.create_all(bind=engine)


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


@app.get("/movies", tags=['Movies'], response_model=List[Movie], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    result = db.query(MovieModel).all()
    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)


@app.get("/movies/{id}", tags=["Movies"], response_model=Movie, responses={404: {"model": str}})
def get_movie_by_id(id: int = Path(ge=0, le=100)) -> Movie:
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
    result = db.query(MovieModel).filter_by(id=id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    result.category = new_movie.category
    result.overview = new_movie.overview
    result.rating = new_movie.rating
    result.title = new_movie.title
    result.year = new_movie.year

    db.commit()

    return JSONResponse(content={"message": "Movie modified"})


@app.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    result = db.query(MovieModel).filter_by(id=id).first()
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    db.delete(result)
    db.commit()

    return JSONResponse(content={"message": "Movie Deleted"})


@app.post("/login", tags=['Auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.model_dump())
        return JSONResponse(content={"jwt": token})
