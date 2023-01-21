#!/usr/bin/env python3
"""
exercise module
"""
import redis
from uuid import uuid4
from functools import wraps
from typing import Union, Optional, Callable


def count_calls(method: Callable) -> Callable:
    """
    Counts the number of times a function is called
    Args:
        method: The function to be decorated
    Returns:
        The decorated function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Counts the number of times a function is called
    Args:
        method: The function to be decorated
    Returns:
        The decorated function
    """
    key = method.__qualname__
    inputs = f"{key}:inputs"
    outputs = f"{key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function for the decorated function
        Args:
            self: The object instance
            *args: The arguments passed to the function
            **kwargs: The keyword arguments passed to the function
        Returns:
            The return value of the decorated function
        """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(data))
        return data

    return wrapper


def replay(method: Callable) -> None:
    """
    Replays the history of a function
    Args:
        method: The function to be decorated
    Returns:
        None
    """
    name = method.__qualname__
    cache = redis.Redis()
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
        Initialize redis client
        Attributes:
            self._redis (redis.Redis): redis client
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores data in redis cache
        Args:
            data (dict): data to store
        Returns:
            str: key
        """
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None)\
            -> Union[str, bytes, int, float]:
        """
        Retrives stored data in redis cache in a desired format
        """
        data = self._redis.get(key)
        if data and fn and callable(fn):
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Get data as string from redis cache
        Args:
            key (str): key
        Returns:
            str: data
        """
        data = self.get(key, lambda x: x.decode('utf-8'))
        return data

    def get_int(self, key: str) -> int:
        """
        Get data as integer from redis cache
        Args:
            key (str): key
        Returns:
            int: data
        """
        data = int(self.get(key))
        return data
