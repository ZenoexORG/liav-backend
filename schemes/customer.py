def customer_scheme(customer) -> dict:
    return {
        'id': str(customer['_id']),
        'user_id': str(customer['user_id']),
        'username': customer['username'],
        'email': customer['email'],
        'password': customer['password'],
        'phone': customer['phone'],
        'admin': customer.get('admin'),
        'credits': customer['credits'],
        'address': customer['address'],
    }

def customers_scheme(customers) -> list:
    return [customer_scheme(customer) for customer in customers]
