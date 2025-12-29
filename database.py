from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "Enter your db key"

engine = create_engine(db_url)


sessionLocal =  sessionmaker(autocommit=False, autoflush=False, bind=engine) 
