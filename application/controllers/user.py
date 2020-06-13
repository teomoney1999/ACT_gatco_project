from gatco.response import json, text
from application.server import app
from application.database import db
from application.extensions import auth, apimanager
from application.models.model import User, Role
import string, random

@app.route("/user_test")
async def user_test(request):
    return text("user_test api")

@app.route("/user/login", methods=["POST", "GET"])
async def user_login(request):
    param = request.json
    user_name = param.get("user_name")
    password = param.get("password")
    print(user_name, password)
    if (user_name is not None) and (password is not None):
        user = db.session.query(User).filter(User.user_name == user_name).first()
        if (user is not None) and auth.verify_password(password, user.password, user.salt):
            auth.login_user(request, user)
            return json({"id": user.id, "user_name": user.user_name, "full_name": user.full_name})
        return json({"error_code":"LOGIN_FAILED","error_message":"user does not exist or incorrect password"}, status=520)

    else:
        return json({"error_code": "PARAM_ERROR", "error_message": "param error"}, status=520)
    return text("user_login api")

@app.route("/user/logout", methods=["GET"])
async def user_logout(request):
    auth.logout_user(request)
    return json({})

@app.route("/user/current_user", methods=["GET"])
async def user_current_user(request):
    user_id = auth.current_user(request)
    print(user_id)

    user = User.query.filter(User.id == user_id).first()
    if user is not None:
        print(user.full_name)
        return json({"id": user.id, "user_name": user.user_name, "full_name": user.full_name})
    else:
        return json({"error_code": "NOT_FOUND", "error_message": "User not found"}, status=520)
    return json({"error_code": "UNKNOWN", "error_message": "Unknown error"}, status=520)

def auth_func(request=None, *kw):
    pass


# def user_register(request=None, Model=None, result=None, *kw):
#     current_user = auth.current_user(request)
#     if current_user is None:
#         return json({'error_code': 'SESSION EXPIRED', 'error_message': 'Session timeout'})
#     if result['id'] is not None:
#         param = request.json
#         role_user = Role.query.filter(Role.role_name == 'user').first()
#         role_employer = Role.query.filter(Role.role_name == 'employer').first()
#         password_info = make_secure_password(param['password'])
#         user = User(user_name=param['user_name'],
#                     password=password_info['secure_password'],
#                     email=param['email'],
#                     salt=password_info['salt'],)
#         if (param['position'] == 'user') or (param['position'] is None):
#             user.roles = [role_user]
#         if param['position'] == 'employer':
#             user.roles = [role_employer]
#
#     pass
#
#
# def make_secure_password(request, password=None):
#     letters = string.ascii_lowercase
#     user_salt = ''.join(random.choice(letters) for i in range(64))
#     secure_password = auth.encrypt_password(password, user_salt)
#     return json({'secure_password': secure_password, 'salt': user_salt})
#

apimanager.create_api(collection_name='user', model=User,
    methods=['GET', 'POST', 'DELETE', 'PUT'],
    url_prefix='/api/v1',
    preprocess=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func], POST=[auth_func], PUT_SINGLE=[auth_func]),
    )