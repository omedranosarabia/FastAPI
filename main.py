from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

movies = [
    {"name": "The Godfather", "year": 1972},
    {"name": "The Shawshank Redemption", "year": 1994},
    {"name": "Schindler's List", "year": 1993},
]


@app.get("/")
def root():
    return HTMLResponse("<h1>Go to /docs</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies
