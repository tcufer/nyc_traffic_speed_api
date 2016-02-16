from flask import current_app, g, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from models import User
# from errors import unauthorized

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password):
    # if current_app.config['USE_TOKEN_AUTH']:
    #     # token authentication
    #     g.user = User.verify_auth_token(username_or_token)
    #     return g.user is not None
    # else:
    #     # username/password authentication
    g.user = User.objects.filter(username=username_or_token).first()
    return g.user is not None and g.user.verify_password(password)


@auth.error_handler
def unauthorized_error():
    return unauthorized('Please authenticate to access this API')


def unauthorized(message):
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': message})
    response.status_code = 401
    return response