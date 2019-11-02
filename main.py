import os
import socket
import logging
import redis
import json
from pymongo import MongoClient
from flask import Flask, request

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

db_client = MongoClient('mongodb://root:password@mongo')
db = db_client.server_storage
storage = db.storage


@app.route('/', endpoint="root")
def put():
    return "Hello, world!"


@app.route('/put', methods=['POST', 'PUT'], endpoint="put")
def put():
    response = {}
    storage.find_one_and_update(
        {"key": request.values.get("key")}, {"$set": {"key": request.values.get("key"), "value": request.values.get("message")}}, upsert=True)
    return response, 200


@app.route('/get', methods=['GET'], endpoint="get")
def get():
    response = {}
    response_code = 200
    if request.values.get("no-cache"):
        storage_ans = storage.find_one({"key": request.values.get("key")})
        if storage_ans:
            response["message"] = storage_ans['value']
        else:
            response_code = 404
    else:
        cached_ans = cache.get(request.values.get("key"))

        if not cached_ans:
            storage_ans = storage.find_one({"key": request.values.get("key")})
            if storage_ans:
                response["message"] = storage_ans['value']
                cache.set(request.values.get("key"), storage_ans["value"])
            else:
                response_code = 200
    return response, response_code


@app.route('/delete', methods=['DELETE'], endpoint="delete")
def get(key):
    response = {}
    response_code = 200
    deleted_count = storage.delete_one({"key": request.values.get("key")}).deleted_count
    if not deleted_count:
        response_code = 404
    return response, response_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=65432)
