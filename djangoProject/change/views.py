from django.shortcuts import render
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
from tools.logging_dec import check_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from change.models import Channel_info
from django.core import serializers
import re
from tools.logging_dec import check_login
from .models import Channel_info
# Create your views here.

""""
http://sailviews.natapp1.cc/api/channel_info
修改通道具体信息视图
（如果单个通道修改，channel_no的数据类型为[i]；如果勾选了同时修改多个通道：channel_no的数据类型为[1,2])
"""

class ChannelView(View):
    #get请求获取全部通道数据
    @check_login
    def get(self, request):
        channels = serializers.serialize('json', Channel_info.objects.all())
        res = json.loads(channels)
        return JsonResponse(res, safe=False, json_dumps_params={'ensure_ascii': False})
    #post请求提交需要修改的通道数据
    @check_login
    def patch(self,request):
        json_str = request.body
        json_obj = json.loads(json_str)
        channel_no=json_obj['channel_no']
        #channel_status=json_obj['channel_status']状态不能改,不传
        address=json_obj['address']
        channel_name=json_obj['channel_name']
        person_status=json_obj['person_status']
        person_sensitive=json_obj['person_sensitive']
        person_frequency=json_obj['person_frequency']
        car_status=json_obj['car_status']
        car_sensitive=json_obj['car_sensitive']
        car_frequency=json_obj['car_frequency']

        if address=="":
            result={'code':402,'error':'修改内容不能为空！'}
            return JsonResponse(result)
        if re.match('rtsp://',address) is None:
            result={'code':403,'error':'修改的地址不符合要求！'}
            return JsonResponse(result)
        if channel_name=="":
            result={'code':404,'error':'修改内容不能为空！'}
            return JsonResponse(result)
        condition = {'channel_no__in': channel_no}
        update_values={
                'address':address,
                'channel_name':channel_name,
                'person_status':person_status,
                'person_sensitive':person_sensitive,
                'person_frequency':person_frequency,
                'car_status': car_status,
                'car_sensitive': car_sensitive,
                'car_frequency': car_frequency,
            }
        try:
            # 批量修改同一数据
            Channel_info.objects.filter(**condition).update(**update_values)
            new_info = serializers.serialize('json', Channel_info.objects.filter(**condition))
            new_info = json.loads(new_info)
            return JsonResponse(new_info, safe=False, json_dumps_params={'ensure_ascii': False})
            # result = {'code': 200, 'msg': '修改成功'}
            # return JsonResponse(result)
        except Exception as e:
            print("报错：%s" % (e))
            result = {'code': 405, 'msg': '修改失败'}
            return JsonResponse(result)


"""
http://sailviews.natapp1.cc/api/reopen
重启通道视图（只是重启通道，不进行信息修改）

"""
class ReopenView(View):
    @check_login
    def patch(self,request):
        json_str = request.body
        json_obj = json.loads(json_str)
        channel_no=json_obj['channel_no'] #channel_no:传列表，通道序号
        reopen=json_obj['reopen']
        if reopen=='1':
            condition = {'channel_no__in': channel_no}
            try:
                #批量修改同一数据
                Channel_info.objects.filter(**condition).update(channel_status='在线')
                result={'code':200,'msg':'重启通道成功','channel_no':channel_no,'channel_status':'在线'}
                return JsonResponse(result)
            except Exception as e:
                print("报错：%s"%(e))
                result={'code':401,'msg':'重启失败'}
                return JsonResponse(result)
        else:
            result = {'code': 401, 'msg': '重启失败'}
            return JsonResponse(result)





        #
        # if len(channel_no)==1:
        #     if channel_no[0] not in [1,2,3,4]:
        #         result={'code':401,'error':'当前通道不存在！'}
        #         return JsonResponse(result)
        #     try:
        #         old_info=Channel_info.objects.get(channel_no=channel_no)
        #         #old_info.channel_status=channel_status 客户端无法修改通道状态
        #         old_info.address = address
        #         old_info.channel_name = channel_name
        #         old_info.person_status = person_status
        #         old_info.person_sensitive = person_sensitive
        #         old_info.person_frequency = person_frequency
        #         old_info.car_status = car_status
        #         old_info.car_sensitive = car_sensitive
        #         old_info.car_frequency = car_frequency
        #         old_info.save()
        #     except Exception as e:
        #         print("错误: %s" % (e))
        #         result={'code':405,'error':'修改信息不符合要求！'}
        #         return JsonResponse(result)
        #     #修改成功：
        #     new_info = serializers.serialize('json',Channel_info.objects.filter(channel_no=1))
        #     new_info=json.loads(new_info)
        #     return JsonResponse(new_info, safe=False, json_dumps_params={'ensure_ascii': False})
        #
        # elif type(channel_no) is list:


