from unittest import result
import cv2 as cv
import numpy as np
import imutils
from config import MIN_CONF, NMS_THRESH, People_Counter
import os
# from main import *


current_host = os.getenv('CURRENT_HOST', 'http://127.0.0.1:8000')

def detect_people(frame, net, ln,personId = 0):
    # print("##### testing #####")
    # print(frame.shape)
    
    H, W, _ = frame.shape
    
    # print("######### done ##########")
    
    results = []
    
    blob = cv.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
        swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)
    #___________________________________we are creating empty lists for each ______
    boxes = []
    centroids = []
    confidences = []
    
    for output in layerOutputs:
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            
            if classID == personId and confidence > MIN_CONF:
                box = detection[0:4] * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                
                
                boxes.append([x, y, int(width), int(height)])
                centroids.append((centerX, centerY))
                confidences.append(float(confidence))
                
    idxs = cv.dnn.NMSBoxes(boxes, confidences, MIN_CONF, NMS_THRESH)
    
    if People_Counter:
        human_count = "Human count: {}".format(len(idxs))
        cv.putText(frame, human_count, (470, frame.shape[0] - 75), cv.FONT_HERSHEY_SIMPLEX, 0.70, (0, 0, 0), 2)
        
    if len(idxs) > 0:
        
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])
            
            r = (confidences[i], (x, y, x + w, y + h), centroids[i])
            results.append(r)
            
    return results