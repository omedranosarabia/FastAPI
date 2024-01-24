from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

movies = [
    {"id": "1", "name": "The Godfather", "year": 1972},
    {"id": "2", "name": "The Shawshank Redemption", "year": 1994},
    {"id": "3", "name": "Schindler's List", "year": 1993},
]


@app.get("/")
def root():
    return HTMLResponse("<h1>Go to /docs</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: int):
    try:
        return movies[movie_id - 1]
    except IndexError:
        return {"error": "Movie not found"}
