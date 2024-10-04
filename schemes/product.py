def product_scheme(product) -> dict:
    return {
        'id': str(product['_id']),
        'provider_id': str(product['provider_id']),
        'name': product['name'],
        'price': product['price'],
        'stock': product['stock'],
        'category': product['category'],
        'imgref': [imgref for imgref in product['imgref']],
    }

def products_scheme(products) -> list:
    return [product_scheme(product) for product in products]
