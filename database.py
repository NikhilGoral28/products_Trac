from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:Nikhil@localhost:5432/products_db"

engine = create_engine(db_url)


sessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine) 