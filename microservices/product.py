from fastapi import APIRouter, HTTPException

from config.database import providers_collection, products_collection
from schemes.product import products_scheme
from models.product import Product
from bson import ObjectId

router = APIRouter(tags=['Product Management'])

def get_products():
    return products_scheme(products_collection.find())

@router.get('/all/')
async def all_products():
    return get_products()

@router.post('/create/')
async def create_product(product: Product):
    existing_product = products_collection.find_one({"name": product.name})
    if existing_product:
        raise HTTPException(status_code=400, detail="Name already registered")
    product_dict = product.model_dump()
    product_dict['imgref'] = [str(url) for url in product_dict['imgref']]

    result = products_collection.insert_one(product_dict)

    product_id = result.inserted_id
    provider_id = product_dict['provider_id']

    if provider_id:
        provider = providers_collection.find_one({'_id': ObjectId(provider_id)})

        if provider:
            products = provider.get('products_id', [])
            products.append(str(product_id))

            providers_collection.update_one(
                {'_id': ObjectId(provider_id)},
                {'$set': {'products_id': products}}
            )

        else:
            raise HTTPException(status_code=404, detail="Provider not found")

    return product

@router.get('/{product_category}/')
async def get_product(product_category: str):
    for product in get_product():
        if product['category'] == product_category:
            return product

@router.put('/{product_id}/')
async def update_product(product_id: str, product: Product):
    product_before_update = products_collection.find_one({'_id': ObjectId(product_id)})

    if not product_before_update:
        raise HTTPException(status_code=404, detail="Product not found")

    update = product.model_dump(exclude_unset=True)
    update['imgref'] = [str(url) for url in update['imgref']]
    result = products_collection.update_one(
        {'_id': ObjectId(product_id)},
        {'$set': update}
    )

    if result.modified_count:
        product = products_collection.find_one({'_id': ObjectId(product_id)})

        return Product(**product)

    else:
        raise HTTPException(status_code=404, detail="Product not found")

@router.delete('/{product_id}/')
async def delete_product(product_id: str):
    product = products_collection.find_one({'_id': ObjectId(product_id)})
    provider_id = product['provider_id']

    if provider_id:
        provider = providers_collection.find_one({'_id': ObjectId(provider_id)})

        if provider:
            products = provider.get('products_id', [])
            products.remove(str(product_id))

            providers_collection.update_one(
                {'_id': ObjectId(provider_id)},
                {'$set': {'products_id': products}}
            )

        else:
            raise HTTPException(status_code=404, detail="Product not found")

    return {'message': 'Product deleted successfully'}
