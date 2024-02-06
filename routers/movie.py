from typing import List
from fastapi import APIRouter, Depends, Path, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from middlewares.jwt_bearer import JWTBearer
from models.movie import Movie, MovieJson
from config.database import session, engine, Base
from services.movie import MovieService

movie_router = APIRouter()

db = session()

Base.metadata.create_all(bind=engine)

movie_service = MovieService(db)


@movie_router.get("/movies", tags=['Movies'], response_model=List[MovieJson], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[MovieJson]:
    result = movie_service.get_movies()
    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)


@movie_router.get("/movies/{id}", tags=["Movies"], response_model=MovieJson, responses={404: {"model": str}})
def get_movie_by_id(id: int = Path(ge=0, le=100)) -> MovieJson:
    '''Get movie by ID'''
    result = movie_service.get_movie_by_id(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)


@movie_router.get("/movies/", tags=["Movies"], response_model=List[MovieJson])
def get_movie_by_category(category: str = Query(min_length=1)) -> List[MovieJson]:
    '''Get movie by Category'''
    result = movie_service.get_movie_by_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    json_result = jsonable_encoder(result)
    return JSONResponse(content=json_result)


@movie_router.post("/movies", tags=["Movies"])
def create_movie(movie_request: MovieJson):
    new_movie = Movie(**movie_request.model_dump())
    movie_service.create_movie(new_movie)

    return JSONResponse(status_code=201, content={"message": "Movie Created"})


@movie_router.put("/movies/{id}", tags=["Movies"])
def modify_movie_by_id(id: int, movie_request: MovieJson):
    new_movie = Movie(**movie_request.model_dump())
    result = movie_service.modify_movie_by_id(id, new_movie)

    if result == "Movie not found":
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    return JSONResponse(content={"message": "Movie modified"})


@movie_router.delete("/movies/{id}", tags=["Movies"])
def delete_movie(id: int):
    result = movie_service.delete_movie(id)
    if result == "Movie not found":
        return JSONResponse(status_code=404, content={"message": "Movie not found"})

    return JSONResponse(content={"message": "Movie Deleted"})
