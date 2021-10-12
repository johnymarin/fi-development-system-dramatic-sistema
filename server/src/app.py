from typing import List

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from server.src.schemas import old_schemas
from server.src.models import old_models
from server.src.crud import old_crud
from .database import SessionLocal, engine
from server.src.routes.old_routes import product_api_router

old_models.Base.metadata.create_all(bind=engine)

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
    BOOKS.append(Book(title="Asus", author="John Mejia", read=True))
    BOOKS.append(
        Book(
            title="Dell",
            author="Johny Marin",
            read=False,
        )
    )
    BOOKS.append(Book(title="HP", author="Cristian Agudelo", read=True))


def _assert_book_id_exists(book_id: int):
    if book_id < 0 or book_id > len(BOOKS):
        raise HTTPException(status_code=404, detail="Comprador not found")


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


@app.get("/pedidos", response_model=ListBooksResponse)
def get_all_books():
    return {"status": "ok", "code": 200, "data": BOOKS}


@app.post("/pedidos", status_code=201, response_model=BookResponse)
def create_book(book: Book):
    BOOKS.append(book)
    return {
        "status": "success",
        "code": 201,
        "messages": ["Book added !"],
        "data": book,
    }


@app.put("/pedido/{book_id}", response_model=BookResponse)
def edit_book(book_id: int, book: Book):
    _assert_book_id_exists(book_id)
    BOOKS[book_id] = book
    return {
        "status": "success",
        "code": 200,
        "messages": ["Book edited !"],
        "data": book,
    }


@app.delete("/pedido/{book_id}", response_model=BookResponse)
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
@app.post("/users/", response_model=old_schemas.User)
def create_user(user: old_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = old_crud.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return old_crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[old_schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = old_crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=old_schemas.User)
def read_user(user_id:int, db: Session = Depends(get_db)):
    db_user = old_crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/user/{user_id}/items/", response_model=old_schemas.Item)
def create_item_for_user(
        user_id: int, item: old_schemas.ItemCreate, db: Session = Depends(get_db)
):
    return old_crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=List[old_schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = old_crud.get_items(db, skip=skip, limit=limit)
    return items


app.include_router(product_api_router, prefix="/productos", tags=["Producto"])


#: Start application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
