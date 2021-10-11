from fastapi import APIRouter, Depends

from typing import List

#from pydantic import BaseModel
from sqlalchemy.orm import Session

from server.src.schemas import old_schemas
from server.src.crud import old_crud
#from .database import SessionLocal, engine
from server.src.database import SessionLocal

product_api_router = APIRouter()



#Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@product_api_router.post("/products", response_model=old_schemas.Product)
def create_product(
        product: old_schemas.ProductCreate, db: Session = Depends(get_db)
):
    return old_crud.create_product(db=db, product=product)


@product_api_router.get("/products/{id}", response_model=old_schemas.Product)
def read_product(
        id: int = id, db: Session = Depends(get_db)
):
    return old_crud.get_product(db=db, id=id)

@product_api_router.get("/products", response_model=List[old_schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = old_crud.get_products(db, skip=skip, limit=limit)
    return products

@product_api_router.put("/prouducts/{id}", response_model=old_schemas.Product)
def update_product(
        product: old_schemas.ProductCreate, id: int = id, db: Session = Depends(get_db)
):
    return old_crud.update_product(db=db, id=id, product=product)




