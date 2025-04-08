from django.http import HttpResponse, HttpResponseNotFound
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
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'  # 添加到程序最开头
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
username_upload=None
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

from .models import Record
def add_record(name,user_upload,create_at,with_helmet,without_helmet):
   Record.objects.create(name=name,user_upload=user_upload,created_at=create_at,with_helmet=with_helmet,without_helmet=without_helmet)


def to_login(request):
    return render(request,'login.html')


def exit(request):
    global username_upload
    request.session["user"]=None
    username_upload=None
    print(request.session["user"])
    return render(request,'login.html')

from django.db import connection
def login(request):
    global username_upload
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
                    username_upload=username
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



import os
import cv2
import time
import threading
from django.conf import settings
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators import gzip
from django.views.decorators.csrf import csrf_exempt
from ultralytics import YOLO

# 全局变量管理
current_frame = None
processing_lock = threading.Lock()

def videodetetct(request):
    return render(request,"video.html")
without_helmet_count = 0
with_helmet_count = 0
@csrf_exempt
def upload_video(request):
    """处理视频上传"""
    global without_helmet_count,with_helmet_count
    if request.method == 'POST' and request.FILES.get('video'):
        video_file = request.FILES['video']
        # 生成唯一文件名
        filename = f"upload_{int(time.time())}{os.path.splitext(video_file.name)[1]}"
        save_path = os.path.join(settings.MEDIA_ROOT, filename)

        # 保存文件
        with open(save_path, 'wb+') as f:
            for chunk in video_file.chunks():
                f.write(chunk)

        # 启动处理线程
        threading.Thread(target=process_video, args=(save_path,)).start()
        return JsonResponse({'status': 'success', 'filename': filename})
    return JsonResponse({'status': 'error', 'message': '无效请求'})

import threading

from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import datetime
#
def process_video(video_path):
    global current_frame, processing_paused, output_video_path, processing_termin, should_terminate
    global without_helmet_count,with_helmet_count
    # 初始化统计器
    without_helmet_count = 0
    with_helmet_count = 0
    seen_ids = set()
    count_lock = threading.Lock()
    id_tracker = {}  # {track_id: last_seen_frame}

    # 生成浏览器可访问的文件名
    timestamp = int(time.time())
    output_filename = f"result_{timestamp}.mp4"
    output_video_path = os.path.join(settings.MEDIA_ROOT, output_filename)
    output_video_url = os.path.join(settings.MEDIA_URL, output_filename)

    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # 使用浏览器兼容编码
    fourcc = cv2.VideoWriter_fourcc(*'avc1')  # 关键修改点
    out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

    if not out.isOpened():
        raise RuntimeError(f"视频编码失败，请安装OpenH264编码器。当前fourcc: {fourcc}")

    try:
        frame_count = 0
        while cap.isOpened():
            with terminate_lock:
                if should_terminate:
                    print("收到终止指令，退出处理")
                    break

            with control_lock:
                if processing_paused:
                    time.sleep(0.1)
                    continue

            ret, frame = cap.read()
            if not ret: break

            # 启用跟踪的预测
            results = model.track(
                source=frame,
                persist=True,
                tracker="bytetrack.yaml",
                stream=True
            )

            for result in results:
                current_frame_ids = set()
                for box in result.boxes:
                    track_id = int(box.id.item()) if box.id is not None else None
                    cls_id = int(box.cls)

                    if track_id is not None:
                        current_frame_ids.add(track_id)
                        id_tracker[track_id] = frame_count

                        # 新ID计数
                        if track_id not in seen_ids:
                            seen_ids.add(track_id)
                            with count_lock:
                                if cls_id == 0:
                                    without_helmet_count += 1
                                elif cls_id == 1:
                                    with_helmet_count += 1

                    # 清理过期ID
                expired_ids = [id for id, last in id_tracker.items()
                               if frame_count - last > 30]
                for id in expired_ids:
                    id_tracker.pop(id, None)
                    seen_ids.discard(id)

                frame_count += 1

                # 生成标注帧并添加统计信息
                annotated_frame = result.plot()

                # 添加统计文字
                with count_lock:
                    display_safe = with_helmet_count
                    display_danger = without_helmet_count

                text = f"佩戴头盔人数: {display_safe}  未佩戴头盔人数: {display_danger}"
                annotated_frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                pil_img = Image.fromarray(annotated_frame_rgb)
                draw = ImageDraw.Draw(pil_img)
                font = ImageFont.truetype("simhei.ttf", 40)

                draw.text((20, 70),  # 位置
                          text,
                          font=font,
                          fill=(0, 255, 0) if display_safe > display_danger else (255, 0, 0))

                # 转换回OpenCV格式
                annotated_frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                # cv2.putText(
                #     annotated_frame,
                #     text,
                #     (20, 70),  # 调整位置
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     1.2,  # 字体大小
                #     (0, 255, 0) if display_safe > display_danger else (0, 0, 255),
                #     3,
                #     cv2.LINE_AA
                # )

                # 写入视频
                with processing_lock:
                    current_frame = annotated_frame
                    out.write(annotated_frame)

            time.sleep(1 / fps)


    finally:
        # 资源释放
        cap.release()
        out.release()
        if os.path.exists(video_path):
            os.remove(video_path)
        processing_termin = False
        should_terminate = False
        create_at=datetime.now()
        print("video_path "+video_path)
        Str=video_path[51:]
        print(Str)
        add_record(Str,username_upload,create_at,with_helmet_count,without_helmet_count)
        print(f"[最终统计] 安全佩戴: {with_helmet_count} | 未佩戴: {without_helmet_count}")
        print("视频处理资源已释放")


#
# def process_video(video_path):
#     global current_frame, processing_paused, output_video_path,processing_termin,should_terminate
#
#     # 生成唯一输出文件名
#     output_video_path = os.path.join(settings.MEDIA_ROOT, f"result_{int(time.time())}.mp4")
#
#     cap = cv2.VideoCapture(video_path)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = cap.get(cv2.CAP_PROP_FPS)
#
#     # 初始化视频写入器
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
#
#     try:
#         while cap.isOpened():
#
#             with terminate_lock:
#
#
#                 if should_terminate:
#                     print("收到终止指令，退出处理")
#                     break
#
#             with control_lock:
#                 if processing_paused:
#                     time.sleep(0.1)
#                     continue
#
#
#             ret, frame = cap.read()
#             if not ret: break
#
#             # YOLO推理
#             results = model.predict(source=frame, stream=True)
#             for result in results:
#                 annotated_frame = result.plot()
#
#                 # 更新全局帧并写入输出文件
#                 with processing_lock:
#                     current_frame = annotated_frame
#                     out.write(annotated_frame)
#
#             time.sleep(1 / fps)  # 按原视频速率处理
#     finally:
#         cap.release()
#         out.release()
#         if os.path.exists(video_path):
#             os.remove(video_path)
#         processing_termin=False
#         should_terminate=False
#         print("视频处理资源已释放")


@gzip.gzip_page
def video_stream(request):
    """生成MJPEG视频流"""

    def generate():
        while True:
            with processing_lock:
                if current_frame is not None:
                    ret, jpeg = cv2.imencode('.jpg', current_frame)
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
            time.sleep(0.01)

    return StreamingHttpResponse(
        generate(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

# views.py
processing_paused = False  # 全局暂停状态
control_lock = threading.Lock()  # 控制状态锁
output_video_path = None  # 输出文件路径

# views.py

@csrf_exempt
def control_view(request):
    """处理暂停/继续请求"""
    print("pause@")
    global processing_paused
    action = request.GET.get('action', '')

    if action not in ['pause', 'resume']:
        return JsonResponse({'status': 'error', 'message': '无效操作'})

    with control_lock:
        processing_paused = (action == 'pause')
    print("pause%%%")
    if processing_paused:
        return JsonResponse({'status': 'paused'})
    else:
        return JsonResponse({'status': 'resume'})

def download_view(request):
    """提供结果视频下载"""
    global output_video_path
    if not output_video_path or not os.path.exists(output_video_path):
        return HttpResponseNotFound("结果文件未生成")

    with open(output_video_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(output_video_path)}"'
        return response


# views.py
import threading

# views.py 全局变量
should_terminate=False
terminate_lock = threading.Lock()  # 独立于暂停控制的锁
@csrf_exempt
def terminate_view(request):
    """安全终止视频处理"""


    global should_terminate
    should_terminate = True
    if request.method != 'POST':
        should_terminate = True
        return JsonResponse({'status': 'error', 'message': '仅支持POST方法'}, status=405)

    with terminate_lock:

        should_terminate = True

    return JsonResponse({'status': 'terminate', 'message': '终止指令已发送'})


from django.shortcuts import render
# 引入响应类
from django.http import HttpResponse







