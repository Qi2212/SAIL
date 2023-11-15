from django.http import JsonResponse
from django.conf import settings
import jwt
from user.models import UserProfile
import hashlib
from django.contrib.sessions.models import Session

#用户登录校验
def check_login(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        # response['Access-Control-Allow-Origin'] = 'https://127.0.0.1:5173'
        # response['Access-Control-Allow-Credentials'] = 'true'
        # return reseponse
        # if not request.COOKIES.get("session_id"):
        #     result = {'code': 700, 'error': '当前无用户登录，请登录！','session_id':request.COOKIES.get("session_id")}
        #     return JsonResponse(result)
        response = JsonResponse({})
        response['Access-Control-Allow-Origin'] = 'https://127.0.0.1:5173'
        response['Access-Control-Allow-Credentials'] = 'true'
        if not request.COOKIES.get("session_id"):
            result = {'code': 700, 'error': '当前无用户登录，请登录！', 'session_id': request.COOKIES.get("session_id")}
            return JsonResponse(result)
        else:
            session_key=request.COOKIES.get("session_id")
            try:
                ssesion = Session.objects.get(session_key=session_key)
            except :
                result = {'code': 701, 'error': '账号登录异常，请重新登录！'}
                return JsonResponse(result)

        return func(*args, **kwargs)
    return wrapper



import os
from django.conf import settings

def delete_image_by_name(image_name):

    image_path = os.path.join(settings.MEDIA_ROOT, image_name)
    # 删除图像文件
    if os.path.exists(image_path):
        os.remove(image_path)


#从路由中获取channel+后续内容的处理函数
from urllib.parse import urlparse
def imagename(url):
    url = url
    parsed_url = urlparse(url)  # 解析URL
    path = parsed_url.path  # 获取URL路径
    # _, file_name = path.rsplit('/', 1)  # 从路径中截取文件名
    channel_no=path.rsplit('/',2)[-2]
    name=file_path = path.rsplit('/',2)[-1]
    file_path = f'{channel_no}\\{name}'
    return file_path  # 输出：'channel1\人数统计-20231009-0312.jpg'






#C:\\Users\\Administrator\\Project\\djangoProject\\media\\channel1\\人数统计

def photopath(all_path):
    all_path = all_path
    #path = "C:\\Users\\Administrator\\Project\\djangoProject\\media\\channel1\\人数统计.jpg"
    # 获取最后一个目录的名称（频道信息）
    channel = os.path.basename(os.path.dirname(all_path))
    print("频道信息:", channel)
    # 获取文件名（不包括频道信息）
    filename = os.path.basename(all_path)
    print("文件名:", filename)
    file_path = f'{channel}\\{filename}'
    return file_path  # 输出：'channel1\人数统计-20231009-0312.jpg'








def transurl_info(photo_urls):
    photo_data = []
    image_list = []
    photos_name = []
    for i in range(1, 5):
        channel_no = i
        photo_dir = f'media/channel{channel_no}'
        photo_files = os.listdir(photo_dir)
        for file in photo_files:
            # pattern = r"人数统计-\d{8}-\d{4}\.jpg"
            photos_name.append(file)
            image_path = f'http://sailviews.natapp1.cc/media/channel{channel_no}/' + file
            image_list.append(image_path)

    for i in range(0, len(image_list)):
        # 获取图片的路由地址
        url = image_list[i]
        # 获取图片名称 取出信息 传参前端
        photo_info = photos_name[i].split("-")
        # 图片名称
        photo_type = photo_info[0]
        # 原始日期
        photo_date = photo_info[1]
        year = photo_date[:4]
        month = photo_date[4:6]
        day = photo_date[6:]

        photo_time = photo_info[2]
        hour = photo_time[:2]
        minute = photo_time[2:4]
        photo_time = f"{year}-{month}-{day} {hour}:{minute}"

        photo_list = {"url": url, "type": photo_type, "time": photo_time}
        photo_data.append(photo_list)

    return photo_data

from django.core.paginator import Paginator
def page_tool(page,photo_data):
    # 分页器实现
    page_number = page
    all_data = list(photo_data)
    paginator = Paginator(all_data, 8)
    page_obj = paginator.get_page(page_number)
    return page_obj
