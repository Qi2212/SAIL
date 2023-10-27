import hashlib
import json
import time
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from user.models import UserProfile
from django.views.decorators.csrf import csrf_exempt
from djangoProject import settings
import jwt
from tools.logging_dec import check_login,post_required,get_required

#用户登录
class LoginView(View):
    def post(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        # 转化过后获取数据
        username = json_obj['username']
        password = json_obj['password']
        if not username or not password:
            result = {'code':401,'error':'请输入用户名或密码！'}
            return JsonResponse(result)
        else:
            try:
                user = UserProfile.objects.get(username=username)
            except Exception:
                result = {'code': 402, 'error': '用户名或密码错误'}
                return JsonResponse(result)
            m = hashlib.md5()
            m.update(password.encode())
            password_m = m.hexdigest()
            if password_m != user.password:
                result = {'code': 403, 'error': '用户名或密码错误'}
                return JsonResponse(result)
            else:
                request.session.set_expiry(60*60*24)
                request.session['username']=username
                result = {'code': 200, 'username':username}
                return JsonResponse(result)

#退出登录,提交POST请求
class LogoutView(View):
    def post(self, request):
        if request.session.get('username'):
            #删除session，退出登录
            del request.session['username']
            result = {'code': 200,'msg':'退出成功'}
            return JsonResponse(result)
        else:
            result = {'code':401,'error':'当前账号未登录'}
            return JsonResponse(result)


