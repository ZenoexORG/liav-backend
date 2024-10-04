from fastapi import APIRouter, HTTPException
from config.database import customers_collection, users_collection
from schemes.customer import customers_scheme
from models.customer import Customer
from bson import ObjectId


router = APIRouter(tags=['Customer Management'])

def get_customers():
    return customers_scheme(customers_collection.find())

@router.get('/all/')
async def all_customers():
    return get_customers()

@router.get('/{customer_email}/')
async def get_customer(customer_email: str):
    for customer in get_customers():
        if customer['email'] == customer_email:
            return customer

@router.put('/{customer_id}/')
async def update_customer(customer_id: str, customer: Customer):
    customer_before_update = customers_collection.find_one({'_id': ObjectId(customer_id)})

    if not customer_before_update:
        raise HTTPException(status_code=404, detail="Customer not found")

    update = customer.model_dump(exclude_unset=True)
    result = customers_collection.update_one(
        {'_id': ObjectId(customer_id)},
        {'$set': update}
    )

    if result.modified_count:
        customer = customers_collection.find_one({'_id': ObjectId(customer_id)})

        if customer['admin'] == False:
            user_data = {
                'username': customer['username'],
                'email': customer['email'],
                'password': customer['password'],
                'phone': customer['phone'],
            }

            users_collection.update_one(
                {'_id': ObjectId(str(customer['user_id']))},
                {'$set': user_data}
            )

            return Customer(**customer)

        elif customer['admin'] == True:
            user_data = {
                'username': customer['username'],
                'email': customer['email'],
                'password': customer['password'],
                'phone': customer['phone'],
                'admin': True
            }

            users_collection.update_one(
                {'_id': ObjectId(str(customer['user_id']))},
                {'$set': user_data}
            )

            customers_collection.delete_one({'_id': ObjectId(customer_id)})

            return {'message': 'Customer deleted from Customers'}

    else:
        raise HTTPException(status_code=404, detail="Customer not found")

@router.delete('/{customer_id}/')
async def delete_customer(customer_id: str):
    customer = customers_collection.find_one({'_id': ObjectId(customer_id)})
    user_id = customer['user_id']

    result = customers_collection.delete_one({'_id': ObjectId(customer_id)})

    if result.deleted_count:
        users_collection.delete_one({'_id': ObjectId(str(user_id))})
        return {'message': 'User and Customer deleted successfully'}

    else:
        raise HTTPException(status_code=404, detail="Customer not found")
