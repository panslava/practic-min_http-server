import redis
import logging
from pymongo import MongoClient, ReturnDocument
from flask import Flask, request

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379)

db_client = MongoClient('mongodb://root:password@mongo')
db = db_client.server_storage
storage = db.storage


@app.route('/')
def root():
    return 'Hello, world!'


@app.route('/put', methods=['PUT'])
def put():
    response = {}
    storage.find_one_and_update(
        {'key': request.values.get('key')},
        {'$set': {'key': request.values.get('key'), 'value': request.values.get('value')}}, upsert=True)
    return response, 200


@app.route('/put', methods=['POST'])
def post():
    response = {}
    status_code = 200
    before = storage.find_one_and_update(
        {'key': request.values.get('key')},
        {'$setOnInsert': {'key': request.values.get('key'), 'value': request.values.get('value')}},
        return_document=ReturnDocument.BEFORE, upsert=True)
    if before is not None:
        status_code = 400
        response = {'ERROR': 'Key already exists'}
    return response, status_code


@app.route('/get', methods=['GET'])
def get():
    response = {}
    response_code = 200
    if request.values.get('no-cache'):
        storage_ans = storage.find_one({'key': request.values.get('key')})
        if storage_ans:
            response['value'] = storage_ans['value']
        else:
            response_code = 404
    else:
        cached_ans = cache.get(request.values.get('key'))
        logging.info(cached_ans)
        if cached_ans:
            if type(cached_ans) is bytes:
                cached_ans = cached_ans.decode('utf-8')
            response['value'] = cached_ans
        else:
            storage_ans = storage.find_one({'key': request.values.get('key')})
            if storage_ans:
                response['value'] = storage_ans['value']
                cache.set(request.values.get('key'), str(storage_ans['value']))
            else:
                response_code = 404

    return response, response_code


@app.route('/delete', methods=['DELETE'])
def delete():
    response = {}
    response_code = 200
    storage.delete_one({'key': request.values.get('key')})
    cache.delete(request.values.get('key'))
    return response, response_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=65432)
