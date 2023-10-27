import json
from django.http import JsonResponse
from django.views import View
import os
from tools.logging_dec import check_login,get_required




#播放本地mp4视频,接收通道码

class PlayView(View):
    @check_login
    def get(self, request):
        json_str = request.body
        json_obj = json.loads(json_str)
        # 转化过后获取数据
        channel_no = json_obj['channel_no']
        video_url = f'http://127.0.0.1:8000/media/video/video{channel_no}.mp4'
        #返回当前通道对应的视频的路由
        return JsonResponse({'code':200,'video_url': video_url})



#展示本地media中图片
class PhotoListView(View):
    @check_login
    def get(self, request):
        photo_base_url = f'http://127.0.0.1:8000/media/'
        photo_list = []
        #获取photo编号为1，2，3，4的图片路由地址
        for i in range(1, 4):
            filename = f'人数统计-2023-10-23-21-40-05-photo{i}.jpg'
            photo_url = os.path.join(photo_base_url, filename)
            photo_list.append(photo_url)
        return JsonResponse({'code':'200','photo_list': photo_list})
