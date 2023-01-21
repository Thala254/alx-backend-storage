#!/usr/bin/env python3
"""
web module
"""
from typing import Callable
import redis
from functools import wraps
import requests


cache = redis.Redis()


def url_count(method: Callable) -> Callable:
    """Wrapper function to count frequency of url"""
    @wraps(method)
    def wrapper(url):
        """Callback function to be returned"""
        cache.incr(f'count:{url}')
        cached_html = cache.get(f'cached:{url}')
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        cache.setex(f'cached:{url}', 10, html)
        return html

    return wrapper


@url_count
def get_page(url: str) -> str:
    """Web cache and tracker"""
    res = requests.get(url)
    return res.text
