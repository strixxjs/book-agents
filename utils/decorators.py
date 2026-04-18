import time
from functools import wraps

def timer(name = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            label = name or func.__name__
            print(f"[Таймер] {label} виконано в {end - start:.2f}s")
            return result
        return wrapper
    return decorator