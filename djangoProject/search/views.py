from django.shortcuts import render

# Create your views here.
import shutil
from django.core.paginator import Paginator
from django.http import JsonResponse,FileResponse
from django.views import View
import json
import re
import os
from datetime import datetime
from tools.logging_dec import check_login,imagename,delete_image_by_name,page_tool,photopath
from django.conf import settings
from django.http import HttpResponse
import zipfile

def convert_datetime_to_string(datetime_str):
    # 将前端传来的日期时间字符串解析为 datetime 对象
    #2023-11-10 20:04
    date_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

    # 使用datetime.strptime()
    # 函数将字符串表示的日期按照指定的格式转换为datetime.date类型的日期对象。
    # 通过这种转换，我们可以使用日期对象的方法和运算符来进行日期的比较、计算和操作。

    # 将 datetime 对象转换为指定格式的字符串
    formatted_date_time = date_time.strftime('%Y%m%d%H%M')

    return formatted_date_time



#已经测试完接口，后续需要不断测试匹配结果是否存在情况缺漏
class PhotosViews(View):
    def post(self, request):
        json_str = request.body  # 拿请求体的数据
        json_obj = json.loads(json_str)

        page = json_obj.get('page',1)
        channel = json_obj.get('channel',"")
        alarm_type = json_obj.get('alarm_type',"")
        start_time = json_obj.get('start_time',"")
        end_time = json_obj.get('end_time',"")


        global start_date, end_date


        if start_time and not end_time:
            start_date = int(convert_datetime_to_string(start_time))
        elif end_time and not start_time:
            end_date = int(convert_datetime_to_string(end_time))
        elif start_time and end_time:
            start_date = int(convert_datetime_to_string(start_time))
            end_date = int(convert_datetime_to_string(end_time))


        if channel == "" and alarm_type == "" and start_time == "" and end_time == "":
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

                # 分页器实现
                page_number = page
                all_data = list(photo_data)
                paginator = Paginator(all_data, 8)
                page_obj = paginator.get_page(page_number)

            length=len(image_list)
            return JsonResponse({
                    'code': 200,
                    'length':length,
                    'photos': list(page_obj),
                })



        # 本地照片目录路径
        #photo_dir = settings.MEDIA_ROOT

        channel_dirs = {
            "1": "channel1",
            "2": "channel2",
            "3": "channel3",
            "4": "channel4",
        }

        alarm_dirs= {
            "people":"人数统计",
            "car":"车辆统计",
        }



        #有点问题，注意为空
        # 例如 "车辆统计-20230910-1003.jpg"
        if alarm_type:
            pattern = r"{alarm_type}-\d{{8}}-\d{{4}}.jpg$".format(alarm_type=alarm_dirs[alarm_type])

        else:
            pattern = r"(\w{4}-\w{8}-\w{4}\.jpg)"

        photos = []
        photo_urls = []

        if channel:
            channel_dir = f'media/{channel_dirs[channel]}'
            channel_name = os.listdir(channel_dir)
            for file_name in channel_name:
                if re.match(pattern, file_name):
                    date_str = file_name.split('-', 1)[-1].split('.')[0]
                    date = int(date_str.replace('-', ''))

                    if not start_time and not end_time:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)

                        if not os.path.isfile(image_path):
                            return JsonResponse({
                                'code': 401,
                                'msg': 'Image not found',
                            })

                    elif not start_time and date <= end_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)

                        if not os.path.isfile(image_path):
                            return JsonResponse({
                                'code': 402,
                                'msg': 'Image not found',
                            })

                    elif not end_time and date >= start_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)

                        if not os.path.isfile(image_path):
                            return JsonResponse({
                                'code': 403,
                                'msg': 'Image not found',
                            })

                    elif date >= start_date and date <= end_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)

                        if not os.path.isfile(image_path):
                            return JsonResponse({
                                'code': 404,
                                'msg': 'Image not found',
                            })

            # photo_list = {}
            # photo_info = []
            # photo_data = []
            # for i in range(0, len(photo_urls)):
            #     url = photo_urls[i]
            #
            #     photo_info = photos[i].split("-")
            #     # 图片名称
            #     photo_type = photo_info[0]
            #     # 原始日期
            #     photo_date = photo_info[1]
            #     year = photo_date[:4]
            #     month = photo_date[4:6]
            #     day = photo_date[6:]
            #
            #     photo_time = photo_info[2]
            #     hour = photo_time[:2]
            #     minute = photo_time[2:4]
            #     photo_time = f"{year}-{month}-{day} {hour}:{minute}"
            #
            #     photo_list = {"url": url, "type": photo_type, "time": photo_time}
            #     photo_data.append(photo_list)
            #
            #     page_obj = page_tool(page, photo_data)
            #
            #     # 返回响应
            # return JsonResponse({
            #     'code': 200,
            #     'photos': list(page_obj),
            # })

        else:
            for i in range(1, 5):
                channel_no = i
                channel_dir = f'media/channel{channel_no}'
                channel_name=os.listdir(channel_dir)
                for file_name in channel_name:
                    if re.match(pattern, file_name):

                        date_str = file_name.split('-', 1)[-1].split('.')[0] #切断


                        date = int(date_str.replace('-', ''))

                        if not start_time and not end_time:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)

                            if not os.path.isfile(image_path):
                                return JsonResponse({
                                    'code': 401,
                                    'msg': 'Image not found',
                                })

                        elif not start_time and date <= end_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)

                            if not os.path.isfile(image_path):
                                return JsonResponse({
                                    'code': 402,
                                    'msg': 'Image not found',
                                })

                        elif not end_time and date >= start_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)

                            if not os.path.isfile(image_path):
                                return JsonResponse({
                                    'code': 403,
                                    'msg': 'Image not found',
                                })

                        elif start_time and end_time and start_date <= date <= end_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)

                            if not os.path.isfile(image_path):
                                return JsonResponse({
                                    'code': 404,
                                    'msg': 'Image not found',
                                })

        photo_list = {}
        photo_info = []
        photo_data = []
        for i in range(0, len(photo_urls)):
            url = photo_urls[i]

            photo_info = photos[i].split("-")
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

        length=len(photo_urls)
        page_obj = page_tool(page,photo_data)
            #返回响应
        return JsonResponse({
                    'code': length,
                    'length': length,
                    'photos':list(page_obj),
                })


#http://sailviews.nataapp1.cc/v1/delete
#删除查询到记录中的图片
class DeleteView(View):
    def delete(self,request):
        json_str = request.body  # 拿请求体的数据
        json_obj = json.loads(json_str)

        channel = json_obj.get('channel', "")
        alarm_type = json_obj.get('alarm_type', "")
        start_time = json_obj.get('start_time', "")
        end_time = json_obj.get('end_time', "")


        global start_date, end_date

        if channel == "" and alarm_type == "" and start_time == "" and end_time == "":
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
            photo_urls=image_list

        if start_time and not end_time:
            start_date = int(convert_datetime_to_string(start_time))
        elif end_time and not start_time:
            end_date = int(convert_datetime_to_string(end_time))
        elif start_time and end_time:
            start_date = int(convert_datetime_to_string(start_time))
            end_date = int(convert_datetime_to_string(end_time))

        # 本地照片目录路径
        # photo_dir = settings.MEDIA_ROOT

        channel_dirs = {
            "1": "channel1",
            "2": "channel2",
            "3": "channel3",
            "4": "channel4",
        }

        alarm_dirs = {
            "people": "人数统计",
            "car": "车辆统计",
        }

        # 有点问题，注意为空
        # 例如 "车辆统计-20230910-1003.jpg"
        if alarm_type:
            pattern = r"{alarm_type}-\d{{8}}-\d{{4}}.jpg$".format(alarm_type=alarm_dirs[alarm_type])

        else:
            pattern = r"(\w{4}-\w{8}-\w{4}\.jpg)"

        photos = []
        photo_urls = []

        if channel:
            channel_dir = f'media/{channel_dirs[channel]}'
            channel_name = os.listdir(channel_dir)
            for file_name in channel_name:
                if re.match(pattern, file_name):
                    date_str = file_name.split('-', 1)[-1].split('.')[0]
                    date = int(date_str.replace('-', ''))

                    if not start_time and not end_time:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)


                    elif not start_time and date <= end_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)


                    elif not end_time and date >= start_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)

                    elif date >= start_date and date <= end_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)

        else:
            for i in range(1, 5):
                channel_no = i
                channel_dir = f'media/channel{channel_no}'
                channel_name = os.listdir(channel_dir)
                for file_name in channel_name:
                    if re.match(pattern, file_name):

                        date_str = file_name.split('-', 1)[-1].split('.')[0]  # 切断

                        date = int(date_str.replace('-', ''))

                        if not start_time and not end_time:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)


                        elif not start_time and date <= end_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)


                        elif not end_time and date >= start_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)

                        elif start_time and end_time and start_date <= date <= end_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)



        #实现删除功能：
        for i in range(0,len(photo_urls)):
            image_name=imagename(photo_urls[i])
            try:
                delete_image_by_name(image_name)
            except Exception as e:
                print("删除过程遇到错误：%s"%(e))
                result={'code':800,"error":"删除请求错误！"}

        return JsonResponse({
            'code': 200,
            'msg':"删除成功！"
        })

        # photo_data = []
        # image_list = []
        # photos_name = []
        # for i in range(1, 5):
        #     channel_no = i
        #     photo_dir = f'media/channel{channel_no}'
        #     photo_files = os.listdir(photo_dir)
        #     for file in photo_files:
        #         # pattern = r"人数统计-\d{8}-\d{4}\.jpg"
        #         photos_name.append(file)
        #         image_path = f'http://sailviews.natapp1.cc/media/channel{channel_no}/' + file
        #         image_list.append(image_path)
        #
        # for i in range(0, len(image_list)):
        #     # 获取图片的路由地址
        #     url = image_list[i]
        #     # 获取图片名称 取出信息 传参前端
        #     photo_info = photos_name[i].split("-")
        #     # 图片名称
        #     photo_type = photo_info[0]
        #     # 原始日期
        #     photo_date = photo_info[1]
        #     year = photo_date[:4]
        #     month = photo_date[4:6]
        #     day = photo_date[6:]
        #
        #     photo_time = photo_info[2]
        #     hour = photo_time[:2]
        #     minute = photo_time[2:4]
        #     photo_time = f"{year}-{month}-{day} {hour}:{minute}"
        #
        #     photo_list = {"url": url, "type": photo_type, "time": photo_time}
        #     photo_data.append(photo_list)
        #
        # page_obj = page_tool(page, photo_data)





#导出图片：以压缩包的形式
#http://sailviews.nataapp1.cc/v1/download
class DownloadView(View):
#导出图片，以压缩包的形式下载
    def post(self, request):
        json_str = request.body  # 拿请求体的数据
        json_obj = json.loads(json_str)

        channel = json_obj.get('channel', "")
        alarm_type = json_obj.get('alarm_type', "")
        start_time = json_obj.get('start_time', "")
        end_time = json_obj.get('end_time', "")

        global start_date, end_date


        if start_time and not end_time:
            start_date = int(convert_datetime_to_string(start_time))
        elif end_time and not start_time:
            end_date = int(convert_datetime_to_string(end_time))
        elif start_time and end_time:
            start_date = int(convert_datetime_to_string(start_time))
            end_date = int(convert_datetime_to_string(end_time))

        #
        # if channel == "" and alarm_type == "" and start_time == "" and end_time == "":
        #     photo_data = []
        #     image_list = []
        #     photos_name = []
        #     for i in range(1, 5):
        #         channel_no = i
        #         photo_dir = f'media/channel{channel_no}'
        #         for file in photo_files:
        #             # pattern = r"人数统计-\d{8}-\d{4}\.jpg"
        #             photos_name.append(file)
        #             image_path = f'http://sailviews.natapp1.cc/media/channel{channel_no}/' + file
        #             image_list.append(image_path)
        #         photo_urls = image_list
        #         photo_files = os.listdir(photo_dir)

        # 本地照片目录路径
        # photo_dir = settings.MEDIA_ROOT

        channel_dirs = {
            "1": "channel1",
            "2": "channel2",
            "3": "channel3",
            "4": "channel4",
        }

        alarm_dirs = {
            "people": "人数统计",
            "car": "车辆统计",
        }

        # 有点问题，注意为空
        # 例如 "车辆统计-20230910-1003.jpg"
        if alarm_type:
            pattern = r"{alarm_type}-\d{{8}}-\d{{4}}.jpg$".format(alarm_type=alarm_dirs[alarm_type])

        else:
            pattern = r"(\w{4}-\w{8}-\w{4}\.jpg)"

        photos = []
        photo_urls = []

        if channel == "" and alarm_type == "" and start_time == "" and end_time == "":
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
                    photo_urls.append(image_path)
                    # image_list.append(image_path)


        elif channel:
            channel_dir = f'media/{channel_dirs[channel]}'
            channel_name = os.listdir(channel_dir)
            for file_name in channel_name:
                if re.match(pattern, file_name):
                    date_str = file_name.split('-', 1)[-1].split('.')[0]
                    date = int(date_str.replace('-', ''))

                    if not start_time and not end_time:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)


                    elif not start_time and date <= end_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)


                    elif not end_time and date >= start_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)



                    elif date >= start_date and date <= end_date:
                        photos.append(file_name)
                        image_path = os.path.join(channel_dir, file_name)
                        url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                        photo_urls.append(url)



        else:
            for i in range(1, 5):
                channel_no = i
                channel_dir = f'media/channel{channel_no}'
                channel_name = os.listdir(channel_dir)
                for file_name in channel_name:
                    if re.match(pattern, file_name):

                        date_str = file_name.split('-', 1)[-1].split('.')[0]  # 切断

                        date = int(date_str.replace('-', ''))

                        if not start_time and not end_time:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)

                        elif not start_time and date <= end_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)


                        elif not end_time and date >= start_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)



                        elif start_time and end_time and start_date <= date <= end_date:
                            photos.append(file_name)
                            image_path = os.path.join(channel_dir, file_name)
                            url = f'http://sailviews.natapp1.cc/media/{channel_dirs[channel]}/' + file_name
                            photo_urls.append(url)




        export_folder = 'C:\\Users\\Administrator\\Project\\djangoProject\\media\\export'
        print(photo_urls)
        image_paths=[]
        #通过循环以及调用imagename函数，image_path就是本机存储的图片的路径
            #image_paths通过循环转化后获得的所有本机的图片路径
        for i in range(0,len(photo_urls)):
            image_name=imagename(photo_urls[i])
            image_path = f'{settings.MEDIA_ROOT}\\{image_name}'
            image_paths.append(image_path)


        zip_filename = 'downloaded_photos.zip'
            #压缩包的路径为:
        zip_path = os.path.join(export_folder, zip_filename)

            #把需要导出的图片文件写入压缩包中
        try:
            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for photo_path_django in image_paths:

                    filename = os.path.basename(photo_path_django)
                    photo_path = os.path.join(export_folder, filename)
                    photoname=photopath(photo_path_django)
                    print(photoname)
                    try:
                        shutil.copy2(photo_path_django, photo_path)
                        zip_file.write(photo_path, arcname=photoname)
                        # response = HttpResponse(open(zip_path, 'rb').read())
                        # response['Content-Type'] = 'application/octet-stream'
                        # response['Content-Disposition'] = 'attachment;filename="downloaded_photos.zip"'
                        # download_path=f'http://sailviews.natapp1.cc/static/download_photos.zip'
                        # return JsonResponse({'code': 200, 'msg': '导出成功！', 'dowload_path': download_path})
                    except Exception as e:
                        print('压缩步骤出现错误：%s' % (e))
                        return JsonResponse({'code': 801, 'error': '压缩图片失败！'})

        except Exception as e:
            print('导出图片时遇到错误：%s'%(e))
            return JsonResponse({'code':802,'error':'导出图片压缩包失败！'})

        response = HttpResponse(open(zip_path, 'rb').read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="downloaded_photos.zip"'
        download_path = f'http://sailviews.natapp1.cc/media/export/downloaded_photos.zip'
        return JsonResponse({'code': 200, 'msg': '导出成功！', 'download_path': download_path})






