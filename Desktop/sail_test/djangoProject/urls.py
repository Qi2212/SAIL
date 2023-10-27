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
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', LoginView.as_view()),
    path('api/logout', LogoutView.as_view()),
    path('api/play/',PlayView.as_view(),name='video'),
    path('api/photos/',PhotoListView.as_view(), name='photo_list'),
    ]

