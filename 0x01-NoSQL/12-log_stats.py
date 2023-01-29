#!/usr/bin/env python3
"""
script that provides some stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def print_nginx_request_logs(nginx):
    '''Prints stats about Nginx request logs.
    '''
    print(f'{nginx.count_documents({})} logs')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print('Methods:')
    for req in methods:
        print(f'\tmethod {req}: {len(list(nginx.find({"method": req})))}')
    status_count = len(list(
        nginx.find({"method": "GET", "path": "/status"})
    ))
    print(f'{status_count} status check')


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)


if __name__ == '__main__':
    run()
