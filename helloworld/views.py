from django.http import HttpResponse
from django.shortcuts import render
from ultralytics import YOLO
from django.http import JsonResponse
from django.shortcuts import render
import cv2
import numpy as np
import torch
from django.db import models
from django.shortcuts import render
from django.http import JsonResponse

import torch
model = YOLO(model=r'C:\Users\hhhh\PycharmProjects\djangoProject1\media\best.pt')  # 全局加载模型一次即可
import cv2
import os
# Create your views here.
import mysql.connector
db = mysql.connector.connect(
    host="localhost",  # MySQL服务器地址
    user="root",   # 用户名
    password="123456",  # 密码
    database="helmet"  # 数据库名称
)

def video(request):
    return render(request,'index2.html')

def photo(request):
    return render(request,'index3.html')

def index(request):
    return render(request,'upload.html')


def index(request):
    return render(request,'upload.html')
def index2(request):
    return render(request,'index2.html')

def register(request):
    return render(request,'register.html')
from .models import User

def register_user(request):
   username=request.POST.get('username')
   password=request.POST.get('password')
   type=request.POST.get('type')
   result=User.objects.filter(name=username)
   if result:
       return render(request, 'register.html',
                     context={"errorInfo": "该用户名已存在", "username":
                         username, "password": password})
   User.objects.create(name=username, password=password,type=type)
   return render(request, "login.html")


def to_login(request):
    return render(request,'login.html')

def exit(request):
    request.session["user"]=None
    print(request.session["user"])
    return render(request,'login.html')

from django.db import connection
def login(request):
    if request.method=="GET":
        return render(request,'login.html')
    else:
        connection.close()
        with connection.cursor() as cursor:
            username = request.POST.get('user')
            password = request.POST.get('password')
            print(username)
            print(password)
            # # 创建游标对象，用于执行SQL查询
            # cursor = db.cursor()
            cursor.execute("SELECT * FROM user")
            results = cursor.fetchall()
            for row in results:
                print("-")
                print(row[1])
                print(row[2])
                print("-")
                if row[1] == username and row[2] == password:

                    request.session["user"]=username
                    print(request.session["user"])
                    # return render(request,"main.html")
                    return render(request, 'upload.html')
    return render(request, 'login.html', {"error": "登录错误"})




def to_upload(request):
    return render(request,'upload.html')

import os
from django.conf import settings
import subprocess

def convert_video(file_path):
    file_name = os.path.basename(file_path)
    output_path = os.path.join(settings.MEDIA_ROOT, 'converted_' + file_name)
    subprocess.run(['ffmpeg', '-i', file_path, '-c:v', 'libx264', output_path])
    return output_path

def remove_after_char(text, char):
    return text.split(char)[0]




def upload(request):
    myFile = request.FILES.get("myfile", None)

    if myFile:

        f = open(os.path.join("C:\\Users\\hhhh\\PycharmProjects\\djangoProject1\\media", myFile.name), "wb+")

        video_url1="media\\"+myFile.name
        video_url2 = "/djangoProject1/media/" + myFile.name
        video_url3 = "C:\\Users\\hhhh\\PycharmProjects\\djangoProject1\\media\\" + myFile.name
        video_url4 = "/djangoProject1/media/runs/detect/detection_v1/" + myFile.name
        request.session['filename']=myFile.name
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()
        # print("))"+video_url1)
        return render(request, 'index3.html', {'video_url1': video_url1,'video_url2':video_url2,'video_url4':video_url4},)
        #return HttpResponse("文件上传成功！")
    else:
        return HttpResponse("没发现文件！")


# tasks.py
from celery import shared_task
import cv2
from ultralytics import YOLO


def detect(request):
    # myFile = request.FILES.get("myfile", None)
    # if myFile:
        name=request.session['filename']
        video_url3 = "C:\\Users\\hhhh\\PycharmProjects\\djangoProject1\\media\\" + name

        model.predict(source=video_url3,
                      project=r"C:\Users\hhhh\PycharmProjects\djangoProject1\media\runs\detect",  # 父目录
                      name="detection_v1",  # 子目录
                      exist_ok=True,  # 允许覆盖
                      save=True,
                      show=False,
                      )
        result=remove_after_char(name,'.')
        result1=result+'.jpg'
        result2 = result + '.avi'
        result3 = result + '.mp4'
        video_url4 = "./media/runs/detect/detection_v1/" +result1
        video_url1 = "./media/runs/detect/detection_v1/" + result2
        video_url2 = "./media/video/" + result3
        print(result2)


        input_file = video_url1

        output_file = video_url2


        cap = cv2.VideoCapture(input_file)


        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


        fourcc = cv2.VideoWriter.fourcc(*'avc1')  # MP4 编码器
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))


        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)


        cap.release()
        out.release()
        video_url2 = "media\\video\\" + name
        del request.session['filename']
        return render(request,'index3.html',{'video_url2':video_url2,'video_url1':video_url1,'video_url4':video_url4})

def upload2(request):
    myFile = request.FILES.get("myfile", None)

    if myFile:

        f = open(os.path.join("C:\\Users\\hhhh\\PycharmProjects\\djangoProject1\\media", myFile.name), "wb+")

        video_url1="media\\"+myFile.name
        video_url2 = "/djangoProject1/media/" + myFile.name
        video_url3 = "C:\\Users\\hhhh\\PycharmProjects\\djangoProject1\\media\\" + myFile.name
        video_url4 = "/djangoProject1/media/runs/detect/detection_v1/" + myFile.name
        request.session['filename']=myFile.name
        for chunk in myFile.chunks():
            f.write(chunk)
        f.close()
        # print("))"+video_url1)
        return render(request, 'index2.html', {'video_url1': video_url1,'video_url2':video_url2,'video_url4':video_url4},)
        #return HttpResponse("文件上传成功！")
    else:
        return HttpResponse("没发现文件！")


# tasks.py
from celery import shared_task
import cv2
from ultralytics import YOLO


def detect2(request):
    # myFile = request.FILES.get("myfile", None)
    # if myFile:
        name=request.session['filename']
        video_url3 = "C:\\Users\\hhhh\\PycharmProjects\\djangoProject1\\media\\" + name

        model.predict(source=video_url3,
                      project=r"C:\Users\hhhh\PycharmProjects\djangoProject1\media\runs\detect",  # 父目录
                      name="detection_v1",
                      exist_ok=True,
                      save=True,
                      show=False,
                      )
        result=remove_after_char(name,'.')
        result1=result+'.jpg'
        result2 = result + '.avi'
        result3 = result + '.mp4'
        video_url4 = "./media/runs/detect/detection_v1/" +result1
        video_url1 = "./media/runs/detect/detection_v1/" + result2
        video_url2 = "./media/video/" + result3
        print(result2)


        input_file = video_url1

        output_file = video_url2


        cap = cv2.VideoCapture(input_file)


        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


        fourcc = cv2.VideoWriter.fourcc(*'avc1')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))


        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)


        cap.release()
        out.release()
        video_url2 = "media\\video\\" + name
        del request.session['filename']
        return render(request,'index2.html',{'video_url2':video_url2,'video_url1':video_url1,'video_url4':video_url4})
