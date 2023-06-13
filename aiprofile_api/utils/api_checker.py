from functools import wraps
from http import HTTPStatus
from flask import request, jsonify


def api_checker(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # if request incoming is http options then return response ok
        if request.method == "OPTIONS":
            return jsonify({
                "status": HTTPStatus.OK,
                "message": "api is alive"
            })

        # otherwise return response
        return func(*args, **kwargs)
    return wrapper

