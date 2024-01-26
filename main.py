from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Movie(BaseModel):
    id: Optional[str]
    name: str = Field(max_length=25, min_length=2)
    year: int = Field(ge=1900, le=2100)
    category: str = Field(max_length=25, min_length=2)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "name": "The Godfather",
                "year": 1972,
                "category": "drama",
            }
        }


movies = [
    {"id": "1", "name": "The Godfather", "year": 1972, "category": "drama"},
    {"id": "2", "name": "The Shawshank Redemption", "year": 1994, "category": "drama"},
    {"id": "3", "name": "Schindler's List", "year": 1993, "category": "drama"},
    {"id": "4", "name": "Raging Bull", "year": 1980, "category": "drama"},
    {"id": "5", "name": "Casablanca", "year": 1942, "category": "drama"},
    {"id": "6", "name": "Godzilla", "year": 1954, "category": "horror"},
    {"id": "7", "name": "La La Land", "year": 2016, "category": "musical"},
    {"id": "8", "name": "King Kong", "year": 1933, "category": "horror"},
    {"id": "9", "name": "The Wizard of Oz", "year": 1939, "category": "musical"},
    {"id": "10", "name": "Van Helsing", "year": 2004, "category": "horror"},
    {"id": "11", "name": "Spiderman", "year": 2002, "category": "action"},
    {"id": "12", "name": "The Dark Knight", "year": 2008, "category": "action"},
    {"id": "13", "name": "Back to the Future", "year": 1985, "category": "action"},
    {"id": "14", "name": "Raiders of the Lost Ark", "year": 1981, "category": "action"},
]


@app.get("/")
def root():
    return HTMLResponse("<h1>Go to /docs</h1>")


@app.get("/movies", tags=["movies"])
def get_movies():
    return movies


@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(
    movie_id: int = Path(
        description="The ID of the movie you want to view", gt=0, lt=200
    )
):
    try:
        return movies[movie_id - 1]
    except IndexError:
        return {"error": "Movie not found"}


@app.get("/movies/", tags=["movies"])
def get_movie_by_category(
    category1: str = Query(min_length=4), category2: str = Query(min_length=4)
):
    movie = [
        movie
        for movie in movies
        if movie["category"] == category1 or movie["category"] == category2
    ]
    return movie


@app.post("/movies", tags=["movies"])
def create_movie(movie: Movie = Body(..., embed=True)):
    movies.append(movie)
    return movies


@app.put("/movies/{movie_id}", tags=["movies"])
def update_movie(movie_id: int, movie: Movie = Body(..., embed=True)):
    try:
        movies[movie_id - 1] = movie
        return movies
    except IndexError:
        return {"error": "Movie not found"}


@app.delete("/movies/{movie_id}", tags=["movies"])
def delete_movie(movie_id: int):
    try:
        del movies[movie_id - 1]
        return movies
    except IndexError:
        return {"error": "Movie not found"}
