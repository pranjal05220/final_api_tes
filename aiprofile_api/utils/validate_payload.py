import json
from functools import wraps
from http import HTTPStatus
from flask import request, jsonify


def validate_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            json.loads(request.get_data())
        except ValueError:
            return jsonify({
                "status": HTTPStatus.BAD_REQUEST,
                "message": "invalid payload"
            })

        # otherwise pass through request
        return func(*args, **kwargs)
    return wrapper

