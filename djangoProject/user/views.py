import hashlib
import json
from django.http import JsonResponse
from django.views import View
from user.models import UserProfile
from djangoProject import settings
from django.contrib.sessions.models import Session



#内网穿透：http://sailviews.natapp1.cc/api/login
class LoginView(View):
    def post(self, request):
        json_obj = json.loads(request.body)
        username = json_obj.get('username')
        password = json_obj.get('password')
        if username == "":
            result = {'code': 401, 'error': '请输入用户名'}
            return JsonResponse(result)
        if password == "":
            result = {'code': 401, 'error': '请输入密码'}
            return JsonResponse(result)
        try:
            user = UserProfile.objects.get(username=username)
        except Exception as e:
            result = {'code': 402, 'error': '用户名不存在'}
            return JsonResponse(result)
        m = hashlib.md5()
        m.update(password.encode())
        password_m = m.hexdigest()
        if password_m != user.password:
            result = {'code': 403, 'error': '用户名或密码错误'}
            return JsonResponse(result)
        else:
            request.session.set_expiry(60 * 60 * 24)
            request.session['username'] = username
            session_id = request.session.session_key
            if session_id is None:
                request.session.save()
                session_id = request.session.session_key
            result = {'code': 200, 'username': username, 'session_id': session_id}
            response = JsonResponse(result)
            response.set_cookie('session_id', session_id,max_age=60*60*24)
            return response


#内网穿透：http://sailviews.natapp1.cc/api/logout
class LogoutView(View):
    def post(self, request):
        if request.COOKIES.get("session_id"):
            session_key = request.COOKIES.get("session_id")
            # 删除用户名和会话ID
            # del request.session['username']
            try:
                sessionid=Session.objects.get(session_key=session_key)
                sessionid.delete()
            except Exception as e:
                result = {'code': 600, 'error': '账号异常登陆，请联系管理员解决'}
                return JsonResponse(result)
            result = {'code': 200, 'msg': '退出成功'}
            response = JsonResponse(result)
            response.delete_cookie('session_id')  # 删除 session_id 的 cookie
            return response
        else:
            result = {'code': 401, 'error': '当前账号未登录'}
            return JsonResponse(result)

