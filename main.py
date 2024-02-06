from fastapi import FastAPI

from routers.movie import movie_router
from routers.user import user_router
from middlewares.error_handler import ErrorHandler

app = FastAPI()
app.title = "My movie API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)
