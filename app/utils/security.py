from flask import request, Response
import json
import jwt
from functools import wraps
import os


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].replace('Bearer ', '')

        if not token:
            return Response(status=401, response=json.dumps({'message': 'token is missing'}), content_type='application/json')

        try:
            jwt.decode(token, os.getenv('SECRET_KEY'))

        except jwt.ExpiredSignatureError:
            return Response(status=403, response=json.dumps({'message': 'token has expired'}), content_type='application/json')
        except jwt.InvalidTokenError:
            return Response(status=403, response=json.dumps({'message': 'token is invalid'}), content_type='application/json')

        return f(*args, **kwargs)
    return decorator
