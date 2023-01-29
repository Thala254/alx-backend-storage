#!/usr/bin/env python3
"""
script that provides some stats about Nginx logs stored in MongoDB
and improves 12-log_stats.py by adding the top 10 of the most present
IPs in the collection nginx of the database logs sorted in desc order.
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


def print_top_ips(server_collection):
    '''Prints statistics about the top 10 HTTP IPs in a collection.
    '''
    print('IPs:')
    request_logs = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        print(f'\t{ip}: {ip_requests_count}')


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_request_logs(client.logs.nginx)
    print_top_ips(client.logs.nginx)


if __name__ == '__main__':
    run()
