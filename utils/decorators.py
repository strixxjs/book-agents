import time
import asyncio
from functools import wraps

def timer(name = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.time()
            result = await func(*args, **kwargs)
            end = time.time()
            label = name or func.__name__
            print(f"[Таймер] {label} виконано в {end - start:.2f}s")
            return result
        return wrapper
    return decorator