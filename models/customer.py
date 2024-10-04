from models.user import User
from models.address import Address

class Customer(User):
    user_id: str
    credits: float
    address: Address
