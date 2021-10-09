import os

from typing import List

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#: Configure CORS
origins = [
    "http://localhost:8080",
    "http://localhost:8081",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



#: Initialize list of books
class Book(BaseModel):
    title: str
    author: str
    read: bool


BOOKS: List[Book] = []


@app.on_event("startup")
async def startup_event():
    BOOKS.clear()
    BOOKS.append(Book(title="On the Road", author="Jack Kerouac", read=True))
    BOOKS.append(
        Book(
            title="Harry Potter and the Philosopher's Stone",
            author="J. K. Rowling",
            read=False,
        )
    )
    BOOKS.append(Book(title="Green Eggs and Ham", author="Dr. Seuss", read=True))


def _assert_book_id_exists(book_id: int):
    if book_id < 0 or book_id > len(BOOKS):
        raise HTTPException(status_code=404, detail="Book not found")


#: Describe all Pydantic Response classes
class ResponseBase(BaseModel):
    status: str
    code: int
    messages: List[str] = []


class PongResponse(ResponseBase):
    data: str = "Pong!"


class BookResponse(ResponseBase):
    data: Book


class ListBooksResponse(ResponseBase):
    data: List[Book]


#: Mount routes
@app.get("/")
def index():
    return {
        "status": "ok",
        "code": 200,
        "data": "Welcome, please check /docs or /redoc",
    }


@app.get("/ping", response_model=PongResponse)
def return_pong():
    return {"status": "ok", "code": 200}


@app.get("/books", response_model=ListBooksResponse)
def get_all_books():
    return {"status": "ok", "code": 200, "data": BOOKS}


@app.post("/books", status_code=201, response_model=BookResponse)
def create_book(book: Book):
    BOOKS.append(book)
    return {
        "status": "success",
        "code": 201,
        "messages": ["Book added !"],
        "data": book,
    }


@app.put("/books/{book_id}", response_model=BookResponse)
def edit_book(book_id: int, book: Book):
    _assert_book_id_exists(book_id)
    BOOKS[book_id] = book
    return {
        "status": "success",
        "code": 200,
        "messages": ["Book edited !"],
        "data": book,
    }


@app.delete("/books/{book_id}", response_model=BookResponse)
def remove_book(book_id: int):
    _assert_book_id_exists(book_id)
    removed_book = BOOKS.pop(book_id)
    return {
        "status": "success",
        "code": 200,
        "messages": ["Book removed !"],
        "data": removed_book,
    }


#users
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id:int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/user/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
        user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

#: Start application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
