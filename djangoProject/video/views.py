import json
from django.http import JsonResponse
from django.views import View
import os
from tools.logging_dec import check_login
import requests
import re
from change.models import *

#播放本地mp4视频,接收通道码
class PlayView(View):
    @check_login
    def get(self, request):

        # channel_no=request.GET.get('channel_no','1')
        # channel=Channel_info.objects.filter(channel_no=channel_no)
        # if channel.channel_status != '开':
        #     result={'code':400,'error':'当前通道还未开启或配置！无法获取录像'}
        #     return JsonResponse(result)
        channel_no = request.GET.get('channel_no', 1)
        channel = Channel_info.objects.filter(channel_no=int(channel_no)).first()

        if channel is None:
            result = {'code': 404, 'error': '未找到匹配的通道'}
            return JsonResponse(result)

        if channel.channel_status != '在线':
            result = {'code': 400, 'error': '当前通道还未开启或配置！无法获取录像'}
            return JsonResponse(result)
        else:
            # 转化过后获取数据
            video_url = f'http://sailviews.natapp1.cc/media/video/video{channel_no}.mp4'
            #返回当前通道对应的视频的路由
            return JsonResponse({'code':200,'video_url': video_url})




#展示本地media中图片
class PhotoListView(View):
    @check_login
    def get(self, request):
        channel_no = request.GET.get('channel_no', 1)
        channel = Channel_info.objects.filter(channel_no=int(channel_no)).first()

        if channel is None:
            result = {'code': 404, 'error': '未找到匹配的通道'}
            return JsonResponse(result)

        if channel.channel_status != '在线':
            result = {'code': 400, 'error': '当前通道还未开启或配置！无法获取图像'}
            return JsonResponse(result)
        # channel_no=request.GET.get('channel_no',1)
        # channel=Channel_info.objects.filter(channel_no=int(channel_no))
        # if channel.channel_status != '在线':
        #     result={'code':400,'error':'当前通道还未开启或配置！无法获取图像'}
        #     return JsonResponse(result)
        else:
            img = os.listdir(f'media/channel{channel_no}')
            #img.remove('__init__.py')
            photo_list = []
            photo_info=[]
            photo_data=[]
            for i in range(0,8):
                photo_url = f'http://sailviews.natapp1.cc/media/channel{channel_no}/' + img[i]
                photo_info=img[i].split("-")
                #图片名称
                photo_type=photo_info[0]
                #原始日期
                photo_date=photo_info[1]
                year = photo_date[:4]
                month = photo_date[4:6]
                day = photo_date[6:]

                photo_time=photo_info[2]
                hour=photo_time[:2]
                minute=photo_time[2:4]
                photo_time = f"{year}-{month}-{day} {hour}:{minute}"

                photo_list={"url":photo_url,"type":photo_type,"time":photo_time}
                photo_data.append(photo_list)
            return JsonResponse({'code':'200','photo_data': photo_data})



""""

photo_base_url = f'http://sailviews.natapp1.cc/media/'
photo_list = []
#获取photo编号为1，2，3，4，5，6，7，8的图片路由地址
for i in range(1, 8):
    filename = f'人数统计-2023-10-23-21-40-05-photo{i}.jpg'
    photo_url = os.path.join(photo_base_url, filename)
    photo_list.append(photo_url)
"""
