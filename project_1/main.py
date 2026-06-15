from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import SessionLocal, engine
from db_models import Base, Product as DBProduct
from schemas import Product
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create tables
Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greet() -> str:
    return "Hello, PROTYUSH GHORUI!"

# ---------------- GET ALL PRODUCTS ----------------
@app.get("/products", response_model=List[Product])
def get_products(db: Session = Depends(get_db)):
    return db.query(DBProduct).all()

# ---------------- GET PRODUCT BY ID ----------------
@app.get("/products/{product_id}", response_model=Product)
def get_product_by_id(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ---------------- CREATE PRODUCT ----------------
@app.post("/products", response_model=Product, status_code=201)
def create_product(product: Product, db: Session = Depends(get_db)):
    exists = db.query(DBProduct).filter(DBProduct.id == product.id).first()
    if exists:
        raise HTTPException(status_code=400, detail="Product already exists")

    db_product = DBProduct(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# ---------------- UPDATE PRODUCT ----------------
@app.put("/products/{product_id}", response_model=Product)
def update_product(
    product_id: int,
    updated: Product,
    db: Session = Depends(get_db)
):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in updated.model_dump().items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

# ---------------- DELETE PRODUCT ----------------
@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
