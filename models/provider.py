from pydantic import BaseModel
from typing import List

from models.address import Address

class Provider(BaseModel):
    name: str
    email: str
    phone: str
    address: Address
    products_id: List[str]
