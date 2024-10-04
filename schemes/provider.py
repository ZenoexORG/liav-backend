def provider_scheme(provider) -> dict:
    return {
        'id': str(provider['_id']),
        'name': provider['name'],
        'email': provider['email'],
        'phone': provider['phone'],
        'address': provider['address'],
        'products_id': [products for products in provider['products_id']],
    }

def providers_scheme(providers) -> list:
    return [provider_scheme(provider) for provider in providers]
