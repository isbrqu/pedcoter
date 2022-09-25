from functools import wraps

def lazy(function):
    """Decorator that makes a property lazy-evaluated.
    Source : https://stevenloria.com/lazy-properties/
    """
    attr_name = "_lazy_" + function.__name__
    @wraps(function)
    def wrapper(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, function(self))
        return getattr(self, attr_name)
    return wrapper

def lazy_with_validation(function):
    """Decorator that makes a property lazy-evaluated.
    Source : https://stevenloria.com/lazy-properties/
    """
    attr_name = "_lazy_" + function.__name__

    @wraps(function)
    def wrapper(self):
        if not hasattr(self, attr_name) or not getattr(self, attr_name):
            setattr(self, attr_name, function(self))
        return getattr(self, attr_name)
    return wrapper

