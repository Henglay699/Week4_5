from functools import wraps
from flask_login import current_user
from flask import abort, flash

def role_required(*rolenames):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not any(current_user.has_role(role) for role in rolenames):
                abort(403)
            return fn(*args, **kwargs)
        return wrapped
    return decorator


def permission_required(permission):
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403)
            return fn(*args, **kwargs)
        return wrapped
    return decorator