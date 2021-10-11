from sqlalchemy.orm import Session

from server.src.schemas import old_schemas
from server.src.models import old_models



def get_user(db: Session, user_id: int):
    user_requested = db.query(old_models.User).filter(old_models.User.id == user_id).first()
    return  user_requested


def get_user_by_email(db: Session, email: str):
    return db.query(old_models.User).filter(old_models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(old_models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: old_schemas.UserCreate):
    fake_hashed_password = user.password + "notrellyhashed"
    db_user = old_models.User(email = user.email, hashed_password = fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(old_models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: old_schemas.ItemCreate, user_id: int):
    db_item = old_models.Item(**item.dict(), owner_id = user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def create_product(db: Session, product: old_schemas.ProductCreate):
    db_product = old_models.Product(
        title=product.title,
        description=product.description,
        price=product.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_product(db: Session, id: int):
    return db.query(old_models.Product).filter(old_models.Product.id == id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(old_models.Product).offset(skip).limit(limit).all()


def update_product(db:Session, id:int, product: old_schemas.ProductCreate):
    product_to_update = db.query(old_models.Product).filter(
        old_models.Product.id == id
    ).first().update(product)
    db.commit()
    db.refresh(product_to_update)
    return product_to_update
