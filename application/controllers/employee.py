from application.extensions import apimanager
from application.models.model import User, Employee
from application.extensions import auth
from gatco.exceptions import ServerError

def auth_func(request=None, **kw):
    #uid = auth.current_user(request)
    #if uid is None:
    #    raise ServerError("abc")
    
    pass

# def user_register(request=None, **kw):
#     pass


apimanager.create_api(collection_name='employee', model=Employee,
    methods=['GET', 'POST', 'DELETE', 'PUT'],
    url_prefix='/api/v1',
    preprocess=dict(GET_SINGLE=[auth_func], GET_MANY=[auth_func], PUT_SINGLE=[auth_func], POST=[auth_func]),
    )
