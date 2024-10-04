from fastapi import APIRouter, HTTPException
from config.database import users_collection, customers_collection
from schemes.user import users_scheme
from models.user import User
from bson import ObjectId

router = APIRouter(tags=['User Management'])

def get_users():
    return users_scheme(users_collection.find())

@router.get('/all/')
async def all_users():
    return get_users()

@router.post('/create/')
async def create_user(user: User):
    existing_user = users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    result = users_collection.insert_one(dict(user))
    user_id = result.inserted_id

    if not user.admin:
        customer_data = {
            **user.model_dump(),
            'user_id': str(user_id),
            'credits': 0.0,
            'address': {
                'street': 'string',
                'city': 'string',
                'state': 'string',
                'zip': 'string',
                'country': 'string'
            }
        }

        customer_data_dict = dict(customer_data)
        customers_collection.insert_one(customer_data_dict)

    return user

@router.get('/{user_email}/')
async def get_user(user_email: str):
    for user in get_users():
        if user['email'] == user_email:
            return user

@router.put('/{user_id}/')
async def update_user(user_id: str, user: User):
    user_before_update = users_collection.find_one({'_id': ObjectId(user_id)})

    if not user_before_update:
        raise HTTPException(status_code=404, detail="User not found")

    update = user.model_dump(exclude_unset=True)
    result = users_collection.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': update}
    )

    if result.modified_count:
        user_after_update = users_collection.find_one({'_id': ObjectId(user_id)})

        if user_after_update['admin'] == False:
            customer_before_update = customers_collection.find_one({'user_id': str(user_id)})

            if not customer_before_update:
                customer_data = {
                    **update,
                    'user_id': str(user_id),
                    'credits': 0.0,
                    'address': {
                        'street': 'string',
                        'city': 'string',
                        'state': 'string',
                        'zip': 'string',
                        'country': 'string'
                    }
                }

                customer_data_dict = dict(customer_data)
                customers_collection.insert_one(customer_data_dict)

            else:
                customers_collection.update_one(
                    {'user_id': str(user_id)},
                    {'$set': {
                        **update,
                        'credits': customer_before_update['credits'],
                        'address': customer_before_update['address'],
                    }}
                )

        elif user_after_update['admin'] == True:
            customers_collection.delete_one({'user_id': str(user_id)})

        return User(**user_after_update)

    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete('/{user_id}/')
async def delete_user(user_id: str):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    user_admin = user['admin']

    result = users_collection.delete_one({'_id': ObjectId(user_id)})

    if result.deleted_count:
        if user_admin == False:
            customers_collection.delete_one({'user_id': str(user_id)})
            return {'message': 'User and Customer deleted successfully'}

        else:
            return {'message': 'User deleted successfully'}

    else:
        raise HTTPException(status_code=404, detail="User not found")
