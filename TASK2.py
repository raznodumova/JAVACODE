from functools import wraps

user_role = None


def set_role(role):
    global user_role
    user_role = role


def access_control(roles=['admin', 'moderator']):
    if roles is None:
        roles = []

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if user_role in roles:
                return func(*args, **kwargs)
            else:
                raise PermissionError
        return wrapper
    
    return decorator