#!/usr/bin/env python3
"""
8-all module
"""
import pymongo


def list_all(mongo_collection):
    """
    list all documents in a collection
    """
    if not mongo_collection:
        return []
    return list(mongo_collection.find())
