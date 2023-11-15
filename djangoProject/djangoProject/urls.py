"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Hom
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from user.views import LoginView,LogoutView
from video.views import PlayView,PhotoListView
from django.conf import settings
from django.conf.urls.static import static
from change.views import ChannelView,ReopenView
from search import views as searchviews
# urls.py
#配置视频和图片文件的映射路由
urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/login', LoginView.as_view()),
                  path('api/logout', LogoutView.as_view()),

                  path('api/play', PlayView.as_view(), name='video'),
                  path('api/play/', PlayView.as_view(), name='video'),

                  path('api/photos', PhotoListView.as_view(), name='photo_list'),
                  path('api/photos/', PhotoListView.as_view(), name='photo_list'),

                  path('api/channel_info/', ChannelView.as_view(), name='channel_info'),
                    path('api/channel_info', ChannelView.as_view(), name='reopen'),

                    path('api/reopen', ReopenView.as_view(), name='reopen'),


                    #查询部分
                  path('v1/photos', searchviews.PhotosViews.as_view()),
                    path('v1/photos/', searchviews.PhotosViews.as_view()),
                    #删除记录
                  path('v1/delete', searchviews.DeleteView.as_view()),
                    #导出图片
                  path('v1/download', searchviews.DownloadView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

""""
登录：
POST        http://sailviews.nataapp1.cc/api/login
退出：
POST        http://sailviews.nataapp1.cc/api/logout

播放通道的视频：不发？默认为?
POST         http://sailviews.nataapp1.cc/api/play

POST         http://sailviews.nataapp1.cc/api/play?channel_no=2


获取通道对应的图片：不发默认 ？channel=1
POST         http://sailviews.nataapp1.cc/api/photos

获取通道对应的图片：
POST         http://sailviews.nataapp1.cc/api/photos?channel_no=2


获取通道的信息：
GET         http://sailviews.nataapp1.cc/api/channel_info

修改通道的信息：
PATCH        http://sailviews.nataapp1.cc/api/channel_info

重启通道：
PATCH        http://sailviews.nataapp1.cc/api/reopen

删除记录图片：
DELETE       http://sailviews.nataapp1.cc/v1/delete

导出图片：
PSOT        http://sailviews.nataapp1.cc/v1/download


"""