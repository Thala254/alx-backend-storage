#!/usr/bin/env python3
"""
exercise module
"""
from redis import Redis
from uuid import uuid4
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a Cache class method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Returns the return value of the decorated function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Stores the history of inputs and outputs for a function i.e method
    Returns value of the decorated function
    """
    key = method.__qualname__
    inputs = f"{key}:inputs"
    outputs = f"{key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Returns the return value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Displays the history of calls of a particular function
    """
    name = method.__qualname__
    cache = Redis()
    calls = cache.get(name).decode('utf-8')
    print(f"{name} was called {calls} times:")
    inputs = cache.lrange(f"{name}:inputs", 0, -1)
    outputs = cache.lrange(f"{name}:outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print(f"{name}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    """
    Defines methods to handle redis cache operations
    """
    def __init__(self) -> None:
        """
        initialize redis client
        """
        self._redis = Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        generates random key and stores input data in Redis
        using the key and returns the key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float]:
        """
        retrives stored data in Redis in a desired format
        """
        data = self._redis.get(key)
        if data and fn and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Get data as string from redis cache
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Get data as integer from redis cache
        """
        data = int(self.get(key))
        return data
