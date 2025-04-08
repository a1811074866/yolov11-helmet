from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
import helloworld.views
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', helloworld.views.index),
    path('index2/', helloworld.views.index2),
    # 配置媒体文件的路由地址
    re_path('media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT},
    name='media'),
    path('tologin/', helloworld.views.to_login),
    path('login', helloworld.views.login),
    path('toupload/', helloworld.views.to_upload),
    path('upload', helloworld.views.upload),
    path('detect', helloworld.views.detect),
    path('upload2', helloworld.views.upload2),
    path('detect2', helloworld.views.detect2),
    path('video/', helloworld.views.video),
    path('photo/', helloworld.views.photo),
    path('index/', helloworld.views.index),
    path('register/', helloworld.views.register),
    path('register_user', helloworld.views.register_user),
    path('exit/', helloworld.views.exit),
    path('videodetect/', helloworld.views.videodetetct),
    path('upload_video/', helloworld.views.upload_video,name='upload_video'),
    path('stream/', helloworld.views.video_stream,name='video_stream'),
    path('control/', helloworld.views.control_view, name='control'),
    path('download/', helloworld.views.download_view, name='download'),
    path('terminate/', helloworld.views.terminate_view, name='terminate'),

]