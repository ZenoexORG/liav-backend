from fastapi import APIRouter, HTTPException
from config.database import providers_collection, products_collection
from schemes.provider import providers_scheme
from models.provider import Provider
from bson import ObjectId


router = APIRouter(tags=['Provider Management'])

def get_providers():
    return providers_scheme(providers_collection.find())

@router.get('/all/')
async def all_providers():
    return get_providers()

@router.post('/create/')
async def create_provider(provider: Provider):
    provider_dict = provider.model_dump()
    provider_dict['products_id'] = []
    result = providers_collection.insert_one(provider_dict)

    return provider

@router.get('/{provider_email}/')
async def get_provider(provider_email: str):
    for provider in get_providers():
        if provider['email'] == provider_email:
            return provider

@router.put('/{provider_id}/')
async def update_provider(provider_id: str, provider: Provider):
    provider_before_update = providers_collection.find_one({'_id': ObjectId(provider_id)})

    if not provider_before_update:
        raise HTTPException(status_code=404, detail="Provider not found")

    update = provider.dict(exclude_unset=True)
    result = providers_collection.update_one(
        {'_id': ObjectId(provider_id)},
        {'$set': update}
    )

    if result.modified_count:
        provider = providers_collection.find_one({'_id': ObjectId(provider_id)})

        return Provider(**provider)

    else:
        raise HTTPException(status_code=404, detail="Provider not found")

@router.delete('/{provider_id}/')
async def delete_provider(provider_id: str):
    provider = providers_collection.find_one({'_id': ObjectId(provider_id)})
    provider_products = provider['products_id']

    result = providers_collection.delete_one({'_id': ObjectId(provider_id)})

    if result.deleted_count:
        for product_id in provider_products:
            products_collection.delete_one({'_id': ObjectId(product_id)})

        return {'message': 'Provider deleted successfully'}

    else:
        raise HTTPException(status_code=404, detail="Provider not found")
