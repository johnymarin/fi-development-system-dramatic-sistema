from fastapi import APIRouter, Depends

from typing import List

#from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import crud, models, schemas
#from .database import SessionLocal, engine
from .database import SessionLocal

product_api_router = APIRouter()



#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@product_api_router.post("/products", response_model=schemas.Item)
def create_product(
        user_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    return crud.create_product(db=db, product=product)



@product_api_router.get("/products", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


