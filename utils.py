from functools import wraps
from typing import Callable


def time_bench(func: Callable):
    import time

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'time benchmark:{func.__name__} {end - start}')

    return wrapper
