from pydantic import BaseModel, HttpUrl
from typing import List

class Product(BaseModel):
    provider_id: str
    name: str
    price: float
    stock: int
    category: str
    imgref: List[HttpUrl]
