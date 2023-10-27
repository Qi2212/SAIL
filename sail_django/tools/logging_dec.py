from django.http import JsonResponse
from django.conf import settings
import jwt
from user.models import UserProfile


#用户登录校验
def check_login(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        if not request.session.get("username"):
            result={'code':501,'error':'当前账号未登录'}
            return JsonResponse(result)
        return func(*args, **kwargs)
    return wrapper



# post请求装饰器，判断请求类型
def post_required(request_type):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.method != 'POST':
                result = {'code': 405, 'error': '无效的请求方法'}
                return JsonResponse(result)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


# get请求装饰器，判断请求类型
def get_required(request_type):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.method != 'GET':
                result = {'code': 405, 'error': '无效的请求方法'}
                return JsonResponse(result)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator