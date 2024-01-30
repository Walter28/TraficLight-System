import math
import html
import os
import time
import ast
from select import select
from .sort import *
import numpy as np
import cv2
import cvzone
import socket
from ultralytics import YOLO

from django.http.response import StreamingHttpResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .camera import VideoCamera
from .models import ENV

isConfigure = None
cameras = {
    0: "E:/TrafficLightVideo/3.mp4",
    1: "E:/TrafficLightVideo/4.mp4",
    2: "E:/TrafficLightVideo/2.mp4",
    3: 0}
VideoCameraObj = {}
size = (1920, 1080)
width, height = size
roadsInfo = {}


def autoCreateRoad():
    for i in range(len(cameras)):
        roadExist = len(ENV.objects.filter(name="road" + str(i + 1)).values())

        # VideoCameraObj["road" + str(i + 1)] = VideoCamera(cameras[i])
        VideoCameraObj["road" + str(i + 1)] = None

        # create Files for video feed
        content = """
        <div class="card-bod" id="video_feed" >
            <!-- style="border: solid #727cf5;" -->
            <img src="{% url 'video_feed_road{{i}}' %}" width="100%" height="100%"/>
        </div>"""
        content = content.replace("{{i}}", str(i + 1))
        file_name = "camview_road{}.html".format(i + 1)

        path = os.path.join(os.getcwd(), "streamapp", "templates", "TrafficManagerTemplate", file_name)
        with open(path, "w") as html_file:
            html_file.write(content)

        if roadExist != 0:
            # pass
            if "road" + str(i + 1) not in roadsInfo.keys():
                roadsInfo["road" + str(i + 1)] = [i, 'Y', '']  # got 3 element : id, TLState, NbOfCar
        else:
            # lambdaEnv = ENV(name="road" + str(i + 1), camera=cameras[i], isConfigure=1, zoneName=file_name,
            #                 zoneDetectionCoord="None")
            lambdaEnv = ENV(name="road" + str(i + 1), zoneName=file_name, zoneDetectionCoord="None")

            lambdaEnv.save()

            roadsInfo["road" + str(i + 1)] = [i, '', '']  # got 3 element : id, NbOfCar,TLState


autoCreateRoad()

nbRoad = ENV.objects.all()

# if len(nbRoad) >= 1:
currentRoad = ENV.objects.first()
isConfigure = currentRoad.getIsConfigure()

nameRoad = ENV.objects.get(name='road1')
nameIn = None


# def detect_connected_cam():
#     global cameras
#
#     for i in range(10):
#         if cv2.VideoCapture(i).isOpened():
#             cameras['cam'+str(i)] = i
#             cv2.VideoCapture().release()
# detect_connected_cam()


# Create your views here
def index(request):
    return render(request, "TrafficManagerTemplate/index.html",
                  {'nameRoad': nameRoad, 'isConfigure': isConfigure, 'current': currentRoad, 'cameras': cameras,
                   'nbRoad': nbRoad})


def setting(request):
    return render(request, "TrafficManagerTemplate/setting.html",
                  {'nameIn': nameIn, 'isConfigure': isConfigure, 'current': currentRoad, 'cameras': cameras,
                   'nbRoad': nbRoad, 'size': size})


def gen(cam='0', road_name=''):
    global VideoCameraObj
    roadMatch = ENV.objects.get(name=road_name)
    road_cam = roadMatch.getCamera()

    # if road_name not in VideoCameraObj:
    #     VideoCameraObj[road_name] = VideoCamera(road_cam)
    VideoCameraObj[road_name] = eval(roadMatch.getVideoCamera())

    # camx = VideoCamera(cam)
    camx = VideoCameraObj[road_name]
    # camx = eval(roadMatch.getVideoCamera())
    className = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
                 "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                 "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
                 "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
                 "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
                 "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
                 "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
                 "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
                 "microwave", "oven", "toster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
                 "teddy bear", "hair drier", "toothbrush"
                 ]

    model = YOLO("../static/Yolo-Weights/yolov8m.pt")

    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

    # limit1 = [400, 260, 750, 265]
    # limit2 = [100, 600, 1000, 650]

    takePhoto = True

    totalCount = []

    filterRoad = ENV.objects.get(name=road_name)
    zoneDetectionCoord = filterRoad.getZoneDetectionCoord()
    # while 1:
    #     print(zoneDetectionCoord)
    if zoneDetectionCoord != "None":
        zoneDetectionCoord = eval(zoneDetectionCoord)  # Convert it to a list first
        zoneDetectionCoord = np.array(zoneDetectionCoord, np.int32)
        zoneDetectionCoord = zoneDetectionCoord.reshape((-1, 1, 2))
        # print(type(height),type(width))
        mask = np.zeros((height, width, 3), dtype=np.uint8)
        mask = cv2.fillPoly(mask, [zoneDetectionCoord], (255, 255, 255))

    while 1:
        # global takePhoto

        frame = camx.get_frame()
        frame = cv2.resize(frame, size)
        if type(zoneDetectionCoord) == np.ndarray:
            frame = cv2.polylines(frame, [zoneDetectionCoord], True, (255, 0, 0))
        stateFeu = camx.get_state_feu(roadsInfo[road_name][0])

        if type(zoneDetectionCoord) == np.ndarray:
            frameWithRegionDetection = cv2.bitwise_and(frame, mask)
        # cv2.imshow("img", frameWithRegionDetection)
        # cv2.waitKey(1)
        # Take a photo is takePhoto ==  True
        if takePhoto:
            road_id = roadsInfo[road_name][0]
            img_name = "road{}Image.jpg".format(road_id + 1)
            photo = frame.copy()
            # SAVE the img in a given DIR, if it doesn't exist create it
            path = os.path.join(os.getcwd(), 'static', 'road_image')

            if not os.path.exists(path):
                os.makedirs(path)
            path_img = os.path.join(path, img_name)
            if not os.path.exists(path_img):
                cv2.imwrite(path_img, photo)

            takePhoto = False

        counter_d = cv2.imread(os.path.join(os.getcwd(), 'static', 'image_TL', 'counter_d.png'),
                               cv2.IMREAD_UNCHANGED)
        red_d = cv2.imread(os.path.join(os.getcwd(), 'static', 'image_TL', 'red.png'),
                           cv2.IMREAD_UNCHANGED)
        green_d = cv2.imread(os.path.join(os.getcwd(), 'static', 'image_TL', 'green.png'),
                             cv2.IMREAD_UNCHANGED)
        yellow_d = cv2.imread(os.path.join(os.getcwd(), 'static', 'image_TL', 'yellow.png'),
                              cv2.IMREAD_UNCHANGED)
        hf, wf, cf = counter_d.shape
        hh, wh, ch = frame.shape
        # frame = cv2.resize(frame, size)
        counter_d = cv2.resize(counter_d, (270, 60))
        red_d = cv2.resize(red_d, (55, 160))
        green_d = cv2.resize(green_d, (55, 160))
        yellow_d = cv2.resize(yellow_d, (55, 160))

        # cv2.imshow(f"image", frame)
        # cv2.waitKey(0)
        print("channel frame : ", frame.shape)
        # print("channel picture : ", counter_d.shape)
        # print("shape red : ", red_d.shape)
        print("RoadsInfo : ", roadsInfo)
        print("statefeu : ", stateFeu)
        print("current : ", road_name)
        print("Nb of object Video : ", VideoCamera.nbOfInter)
        # print("height: ", height)
        print("Take photo : ", takePhoto)
        print("VideoCam : ", VideoCameraObj)
        print("Road Cam : ", road_cam)

        # puting the image on the frame
        frame = cvzone.overlayPNG(frame, counter_d, [10, 10])

        # PUT the road ID
        cv2.putText(frame, str(roadsInfo[road_name][0] + 1), (240, 48), cv2.FONT_HERSHEY_DUPLEX, fontScale=0.8,
                    color=(0, 0, 255), thickness=4)

        # Putting TL State in the frame
        if stateFeu == 'V':
            frame = cvzone.overlayPNG(frame, green_d, [300, 5])
        if stateFeu == 'R':
            frame = cvzone.overlayPNG(frame, red_d, [300, 5])
        if stateFeu == 'Y':
            frame = cvzone.overlayPNG(frame, yellow_d, [300, 5])
        # frame[50:50, 20:240] = red_design

        # Fill the raodsInfo dict by setting the TLState
        # for x in range(len(nbRoad)):
        # if x==0:
        roadsInfo[road_name][1] = stateFeu
        roadsInfo[road_name][2] = len(totalCount)

        # DIFFERENT TRAITEMENT ON  THE FRAME
        # We send the frame with detection zone filtered, for detctions
        if type(zoneDetectionCoord) == np.ndarray:
            results = model(frameWithRegionDetection, stream=True)
        else:
            results = model(frame, stream=True)

        detections = np.empty((0, 5))

        for r in results:
            boxes = r.boxes
            for box in boxes:
                # bounding box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                w, h = x2 - x1, y2 - y1
                bbox = (x1, y1, w, h)
                # the confidence
                conf = math.ceil((box.conf[0] * 100))
                # the className
                cls = int(box.cls[0])
                currentClass = className[cls]

                # NUmber of detections using __len__() func from Results class
                cv2.putText(frame, str(r.__len__()), (110, 48), cv2.FONT_HERSHEY_DUPLEX, fontScale=0.8,
                            color=(0, 0, 253), thickness=2)

                # if className[cls] == 'car' or className[cls] == 'bus' or className[cls] == 'truck' \
                #         or className[cls] == 'motorbike':
                if className[cls] != 'person' and className[cls] != 'clock':
                    # if className[cls] in className:
                    cvzone.cornerRect(frame, (x1, y1, w, h), t=3, l=12, rt=1, colorR=(255, 0, 0))

                    # print the confidence on the video frame
                    cvzone.putTextRect(frame, f'{conf}% {className[cls]}', (x1, y1 - 20), scale=0.6, thickness=1,
                                       colorT=(255, 255, 255), colorR=(0, 0, 0), font=cv2.FONT_HERSHEY_DUPLEX)

                    # currentArray = np.array([x1, y1, x2, y2, conf])
                    # detections = np.vstack((detections, currentArray))

        # resultsTracker = tracker.update(detections)

        # in car line
        # cv2.line(frame, (limit1[0], limit1[1]), (limit1[2], limit1[3]), (0, 0, 255), thickness=3)
        # out car line
        # cv2.line(frame, (limit2[0], limit2[1]), (limit2[2], limit2[3]), (0, 0, 255), thickness=3, lineType=cv2.LINE_AA)

        # for result in resultsTracker:
        #     x1, y1, x2, y2, id = result
        #     x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
        #     w, h = x2 - x1, y2 - y1
        #     # print(result)
        #     cvzone.cornerRect(frame, (x1, y1, w, h), t=3, l=12, rt=1, colorR=(255, 0, 0))
        #     cvzone.putTextRect(frame, f'N0 {id}', (x1, y1 - 10), scale=1, thickness=1, offset=5, colorT=(255, 255, 255),
        #                        colorR=(0, 0, 0))
        #     if id in totalCount:
        #         cv2.circle(frame, (x1, y1), 7, (0, 255, 0), cv2.FILLED)
        #     cx, cy = x1 + w // 2, y1 + h + 0 // 2
        #     cv2.circle(frame, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        #
        #     # if a car touch the entrance line
        #     if limit1[0] < cx < limit1[2] and limit1[1] - 5 < cy < limit1[3] + 5:
        #         if totalCount.count(id) == 0:
        #             totalCount.append(id)
        #         # touched in : car line
        #         cv2.line(frame, (limit1[0], limit1[1]), (limit1[2], limit1[3]), (0, 255, 0), thickness=3)
        #
        #     # if a car touch the exit line
        #     if limit2[0] < cx < limit2[2] and limit2[1] - 5 < cy < limit2[3] + 5:
        #         if totalCount.count(id) == 1:
        #             if len(totalCount) != 0:
        #                 totalCount.remove(id)
        #                 # touched in : car line
        #         cv2.line(frame, (limit2[0], limit2[1]), (limit2[2], limit2[3]), (0, 255, 0), thickness=3)

        # Write the number of cars counted
        countPosition = []
        # cv2.putText(frame, str(len(totalCount)), (105, 53), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 255), thickness=4)

        # frame = cv2.flip(frame, 1)
        # we must encode our frame into jpge in order to correctly display it in the web
        jpge = cv2.imencode('.jpe', frame)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpge + b'\r\n\r\n')


# def video_feed(request):
#     global isConfigure
#     if isConfigure:
#         return StreamingHttpResponse(gen(currentRoad.getCamera()),
#                                      content_type='multipart/x-mixed-replace; boundary=frame')

def gen_video_feed():
    video_feeds = []
    for i in range(len(nbRoad)):
        func_name = "video_feed_road{}".format(i + 1)
        road_cam = ENV.objects.all()[i].getCamera()
        road_name = ENV.objects.all()[i].getName()
        isConfigure = ENV.objects.all()[i].getIsConfigure()
        content = """def {{name_func}}(request):
                             return StreamingHttpResponse(gen("{{cam}}","{{road}}"),
                                                          content_type='multipart/x-mixed-replace; boundary=frame')"""
        content = content.replace("{{name_func}}", str(func_name))
        content = content.replace("{{cam}}", str(road_cam))
        # content = content.replace("{{conf}}", str(isConfigure))
        content = content.replace("{{road}}", str(road_name))
        video_feeds.append(content)
    return video_feeds


def change_road(request):
    global currentRoad
    global isConfigure
    global nameIn

    # if 'option' in request.GET['option']:
    name_road = request.GET['option']
    roadMatch = ENV.objects.get(name=name_road)
    idRoad = roadMatch.getId()
    zoneName = roadMatch.getZoneName()

    currentRoad = ENV.objects.get(id=idRoad)
    isConfigure = currentRoad.getIsConfigure()

    if not isConfigure:
        # VideoCamera().__del__()
        html = render_to_string('TrafficManagerTemplate/defaultcamzone.html', {'cameras': cameras})
    else:
        path = 'TrafficManagerTemplate/' + zoneName
        html = render_to_string(path)

    return HttpResponse(html)


def page_load(request):
    global currentRoad
    global isConfigure
    global takePhoto
    takePhoto = True

    roadMatch = ENV.objects.get(name=currentRoad)
    zoneName = roadMatch.getZoneName()

    if not isConfigure:
        html = render_to_string('TrafficManagerTemplate/defaultcamzone.html', {'cameras': cameras})
    else:
        # while 1:
        #     print(roadMatch.getCamera())
        path = 'TrafficManagerTemplate/' + zoneName

        html = render_to_string(path)

    return HttpResponse(html)


def road_set_camera(request):
    global currentRoad

    roadMatch = ENV.objects.get(name=currentRoad)
    road_name = roadMatch.getName()

    cam_id = request.GET['option']

    env = ENV.objects.get(name=road_name)
    env.camera = cam_id
    env.isConfigure = 1
    if len(cam_id) == 1:
        env.videoCamera = "VideoCamera({})".format(cam_id)
    else:
        env.videoCamera = "VideoCamera('{}')".format(cam_id)
    env.save()

    return HttpResponse(' Camera setted avec success')


# def frame_size(request):
#     global width
#     global height
#     # width = request.GET['width']
#     # height = request.GET['height']
#     return HttpResponse(" bien recu les taille")


def road_take_photo(request):
    # global takePhoto
    # takePhoto = True

    road_name = request.GET['option']
    img_name = road_name + "Image.jpg"
    path = os.path.join(os.getcwd(), 'static', 'road_image', img_name)
    if os.path.exists(path):
        response = "<img id=\"img\" src='../static/road_image/{}' />".format(img_name)
    else:
        response = "NaN"
    return HttpResponse(response)


def receive_coord(request):
    coord = request.GET['coord']
    road_name = request.GET['road_name']

    env = ENV.objects.get(name=road_name)
    env.zoneDetectionCoord = coord
    env.save()

    response = "Bien recu coord {} from {}".format(coord, road_name)

    return HttpResponse(response)


video_feed_elt = gen_video_feed()
# print(len(video_feed_elt))
for x in video_feed_elt:
    tree = ast.parse(x)
    # print(ast.dump(tree))
    exec(compile(tree, filename="", mode="exec"))

# def video_feed_road1(request):
#     return StreamingHttpResponse(gen("0", "road1"), content_type='multipart/x-mixed-replace; boundary=frame')
#
#
# def video_feed_road2(request):
#     return StreamingHttpResponse(gen("0", "road2"), content_type='multipart/x-mixed-replace; boundary=frame')
#
#
# def video_feed_road3(request):
#     return StreamingHttpResponse(gen("0", "road3"), content_type='multipart/x-mixed-replace; boundary=frame')
#
#
# def video_feed_road4(request):
#     return StreamingHttpResponse(gen("0", "road4"), content_type='multipart/x-mixed-replace; boundary=frame')
