import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render
from datetime import datetime
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
import base64
import pandas as pd #pandas to read and explore dataset
import numpy as np
import io
import matplotlib.pyplot as plt
import cv2
from ultralytics import YOLO

global username, yolo_model

#yolo confidence threshold to detect animal species
CONFIDENCE_THRESHOLD = 0.50
GREEN = (0, 255, 0)

yolo_model = YOLO("model/best.pt")
print("Yolo Model Loaded")

def TrainYolo(request):
    if request.method == 'GET':
        cnn_train_detection = cv2.imread("model/result.png")
        plt.figure(figsize=(12, 7))
        plt.imshow(cnn_train_detection)
        plt.title("YoloV8 Animal Species Detection Performance")
        plt.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        #plt.clf()
        #plt.cla()
        #plt.close()
        context= {'data':"YoloV8 Animal Species Detection Performance", 'img': img_b64}
        return render(request, 'UserScreen.html', context)

def TrainGraph(request):
    if request.method == 'GET':
        cnn_train_detection = cv2.imread("model/results.png")
        plt.figure(figsize=(12, 7))
        plt.imshow(cnn_train_detection)
        plt.title("YoloV8 Animal Species Detection Training Graph")
        plt.axis('off')
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        #plt.clf()
        #plt.cla()
        #plt.close()
        context= {'data':"YoloV8 Animal Species Detection Training Graph", 'img': img_b64}
        return render(request, 'UserScreen.html', context)

def detectAnimal(frame):
    global yolo_model
    labels = ['antelope', 'badger', 'bat', 'bear', 'beaver', 'beetle', 'bison', 'black bear', 'boar',
              'bobcat', 'buffalo', 'butterfly', 'crow', 'fish', 'honeybee', 'koala', 'pig', 'polar bear', 'zebra']
    detections = yolo_model(frame)[0]
    # loop over the detections
    for data in detections.boxes.data.tolist():
        print(data)
        # extract the confidence (i.e., probability) associated with the detection
        confidence = data[4]
        cls_id = data[5]
        # filter out weak detections by ensuring the 
        # confidence is greater than the minimum confidence
        if float(confidence) >= CONFIDENCE_THRESHOLD:
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            cv2.rectangle(frame, (xmin, ymin) , (xmax, ymax), GREEN, 2)
            cv2.putText(frame, labels[int(cls_id)], (xmin, ymin-10),  cv2.FONT_HERSHEY_SIMPLEX,0.7, (255, 0, 0), 2)            
    return frame    

def SpeciesDetectionAction(request):
    if request.method == 'POST':
        filename = request.FILES['t1'].name
        image = request.FILES['t1'].read() #reading uploaded file from user
        if os.path.exists("SpeciesApp/static/"+filename):
            os.remove("SpeciesApp/static/"+filename)
        with open("SpeciesApp/static/"+filename, "wb") as file:
            file.write(image)
        file.close()
        img = cv2.imread("SpeciesApp/static/"+filename)
        img = detectAnimal(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #img = cv2.resize(img, (600,300))#display image with predicted output
        plt.imshow(img)
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        img_b64 = base64.b64encode(buf.getvalue()).decode()
        #plt.clf()
        #plt.cla()
        #plt.close()
        context= {'data':"Animal Species Detected Output", 'img': img_b64}
        return render(request, 'UserScreen.html', context)

def SpeciesDetection(request):
    if request.method == 'GET':
        return render(request,'SpeciesDetection.html', {})     

def index(request):
    if request.method == 'GET':
        return render(request,'index.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def UserLoginAction(request):
    if request.method == 'POST':
        global username, contract, usersList
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            output = 'Welcome '+username
            context= {'data':output}
            return render(request, "UserScreen.html", context)
        if status == 'none':
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)
        


        


        
