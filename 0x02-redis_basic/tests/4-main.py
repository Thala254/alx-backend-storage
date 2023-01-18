#!/usr/bin/env python3
"""
4-main file
"""
import redis

Cache = __import__('exercise').Cache
replay = __import__('exercise').replay

cache = Cache()
cache.store("foo")
cache.store("bar")
cache.store(42)
replay(cache.store)
