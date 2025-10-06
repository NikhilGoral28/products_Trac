from fastapi import FastAPI,Depends
from models import Product
from database import sessionLocal, engine
import database_model
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
database_model.Base.metadata.create_all(bind=engine)


@app.get("/") 
def greet():
    return "Hello, welcome to the Product Trac!"
 

products_dict = [
    Product(id=1,name="Laptop",Description="A high-performance laptop",price= 999.99,quantity=10),
    Product(id=2,name="Smartphone",Description="A latest model smartphone",price=699.99,quantity=25),
    Product(id=3,name="Headphones",Description="Noise-cancelling headphones",price=199.99,quantity=50),
]

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    db = sessionLocal()

    count = db.query(database_model.Product).count
    # If the table is empty, populate it with initial data 
    
    if count == 0:

        for product in products_dict:
            db.add(database_model.Product(**product.model_dump()))

        db.commit()
init_db()

@app.get("/products") 
def get_all_products(db: Session = Depends(get_db)):
    db_products = db.query(database_model.Product).all()
    return db_products

@app.get("/products/{product_id}")
def get_product_by_id(product_id: int,db: Session = Depends(get_db)):

    db_products = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_products:
        return db_products
    raise HTTPException(status_code=404, detail="Product not found")
  
@app.post("/products")
def add_products(product: Product, db: Session = Depends(get_db)):
    db.add(database_model.Product(**product.model_dump()))
    db.commit()
    return product

@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product, db: Session = Depends(get_db)):
    db_products = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()

    if db_products:
        db_products.name = updated_product.name 
        db_products.Description = updated_product.Description
        db_products.price = updated_product.price
        db_products.quantity = updated_product.quantity
        db.commit()
        return "Product Updated"
    else:
        raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int,db:Session = Depends(get_db)):
    db_products = db.query(database_model.Product).filter(database_model.Product.id == product_id).first()
    if db_products:
        db.delete(db_products)
        db.commit()
        return "Product Deleted"
    else:
        raise HTTPException(status_code=404, detail="Product not found")