from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
import os

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


@app.get("/movies", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200, content=movies)


@app.get("/movies/{movie_id}", tags=["movies"], response_model=Movie, status_code=200)
def get_movie(
    movie_id: int = Path(
        description="The ID of the movie you want to view", gt=0, lt=200
    )
) -> Movie:
    try:
        return JSONResponse(status_code=200, content=movies[movie_id - 1])
    except IndexError:
        return JSONResponse(status_code=404, content={"error": "Movie not found"})


@app.get("/movies/", tags=["movies"], response_model=List[Movie], status_code=200)
def get_movie_by_category(
    category1: str = Query(min_length=4), category2: str = Query(min_length=4)
) -> List[Movie]:
    movie = [
        movie
        for movie in movies
        if movie["category"] == category1 or movie["category"] == category2
    ]

    return JSONResponse(status_code=200, content=movie)


@app.post("/movies", tags=["movies"], response_model=dict, status_code=201)
def create_movie(movie: Movie = Body(..., embed=True)) -> dict:
    movies.append(movie.model_dump())
    return JSONResponse(
        status_code=201, content={"message": "Movie created successfully"}
    )


@app.put("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def update_movie(movie_id: int, movie: Movie = Body(..., embed=True)) -> dict:
    try:
        movies[movie_id - 1] = movie
        return JSONResponse(
            status_code=200, content={"message": "Movie updated successfully"}
        )
    except IndexError:
        return JSONResponse(status_code=404, content={"error": "Movie not found"})


@app.delete("/movies/{movie_id}", tags=["movies"], response_model=dict, status_code=200)
def delete_movie(movie_id: int) -> dict:
    try:
        del movies[movie_id - 1]
        return JSONResponse(
            status_code=200, content={"message": "Movie deleted successfully"}
        )
    except IndexError:
        return JSONResponse(status_code=200, content={"error": "Movie not found"})


@app.post("/ask", tags=["model"])
def ask_model(question) -> dict:
    os.environ["OPENAI_API_KEY"] = "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"

    embeddings = OpenAIEmbeddings()

    CHROMA_INDEX_NAME = "./instruct-incapacidad"

    vectorstore = Chroma(
        persist_directory=CHROMA_INDEX_NAME, embedding_function=embeddings
    )

    chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    chain_answer = RetrievalQA.from_chain_type(
        llm=chat,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    )

    answer = chain_answer.invoke(question)

    return JSONResponse(
        status_code=201, content={"response": answer['result']}
    )
