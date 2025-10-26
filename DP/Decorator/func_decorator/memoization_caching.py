def memoize(func):
    cache = {}

    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result

        return result

    return wrapper


@memoize
def fibo(n):
    if n < 2:
        return n
    return fibo(n - 1) + fibo(n - 2)


print(fibo(8))

# built-in version in Python
from functools import lru_cache


@lru_cache(maxsize=None)
def fibo(n):
    if n < 2:
        return n
    return fibo(n - 1) + fibo(n - 2)


print(fibo(8))
