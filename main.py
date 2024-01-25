from fastapi import FastAPI, Body
from fastapi.responses import HTMLResponse

app = FastAPI()

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
def get_movie(movie_id: int):
    try:
        return movies[movie_id - 1]
    except IndexError:
        return {"error": "Movie not found"}


@app.get("/movies/", tags=["movies"])
def get_movie_by_category(category1: str, category2: str):
    movie = [
        movie
        for movie in movies
        if movie["category"] == category1 or movie["category"] == category2
    ]
    return movie


@app.post("/movies", tags=["movies"])
def create_movie(name: str = Body(), year: int = Body(), category: str = Body()):
    movie = {
        "id": str(len(movies) + 1),
        "name": name,
        "year": year,
        "category": category,
    }
    movies.append(movie)
    return movies


@app.put("/movies/{movie_id}", tags=["movies"])
def update_movie(
    movie_id: int, name: str = Body(), year: int = Body(), category: str = Body()
):
    try:
        movies[movie_id - 1]["name"] = name
        movies[movie_id - 1]["year"] = year
        movies[movie_id - 1]["category"] = category
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
