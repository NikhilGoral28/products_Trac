from pydantic import BaseModel

class Product(BaseModel):
    id: int
    name: str
    Description: str
    price: float
    quantity: int
