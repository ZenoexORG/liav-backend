def user_scheme(user) -> dict:
    return {
        'id': str(user['_id']),
        'username': user['username'],
        'email': user['email'],
        'password': user['password'],
        'phone': user['phone'],
        'admin': user.get('admin', True)
    }

def users_scheme(users) -> list:
    return [user_scheme(user) for user in users]
