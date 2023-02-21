import cv2 as cv
from cv2 import INTER_AREA
import numpy as np
import imutils
import os
import pafy
from scipy.spatial import distance as dist
from imutils.video import VideoStream, FPS
from config import *
from detection import *
from verify_params import *


# VerifyValidateParams.create_folders_if_doesnot_exist()

def social_distancing(video_url):
    video = pafy.new(video_url)
    # best = video.getbest(preftype="mp4")
    file_name=video_url.split('/')[-1][:5]


    labelsPath = "yolo/coco.names"
    LABELS = open(labelsPath).read().strip().split("\n")

    # ###############################################################################print(LABELS)
    weights = "yolo/yolov3.weights"
    configofyolo = "yolo/yolov3.cfg"


    net  = cv.dnn.readNetFromDarknet(configofyolo,weights)

    ln = net.getLayerNames()
    ln = [ln[int(i) - 1] for i in net.getUnconnectedOutLayers()]

    ##_____________________________________________Capturing video file ____________________________
    writer = None
    fps = FPS().start()
    capture = cv.VideoCapture()
    video_cod = cv.VideoWriter_fourcc(*'XVID')
    frame_width = int(capture.get(3))
    frame_height = int(capture.get(4))
    size = (frame_width, frame_height)
    video_output = cv.VideoWriter(f"static/output/{file_name}.avi",video_cod,10,size)

    # print(capture.read())
    # print(type(capture.read()))
    # print("===========")
    # for x in capture.read():
    #     print("#### ")
    #     print(type(x))
        
    #     # print(y)
    #     print("$$$$$$")
    # isTrue, frame = capture.read()
    # print(len(frame))
    # i = 0
    f_c = int(capture.get(cv.CAP_PROP_FRAME_COUNT))
    while f_c != 0:
        isTrue, frame = capture.read()
        # print(frame)
        # frame = cv.resize(frame, (1000,500))
        # print(frame.shape)
        
        results = detect_people(frame, net, ln,personId=LABELS.index("person"))
        
        # if False:
            
        #     break
        
        
        serious = set()
        abnormal = set()

        if len(results) >= 2:
            centroids = np.array([r[2] for r in results])
            D = dist.cdist(centroids, centroids, metric="euclidean")

            # loop over the upper triangular of the distance matrix
            for i in range(0, D.shape[0]):
                for j in range(i + 1, D.shape[1]):
                    # check to see if the distance between any two
                    # centroid pairs is less than the configured number of pixels
                    if D[i, j] < MIN_DISTANCE:
                        # update our violation set with the indexes of the centroid pairs
                        serious.add(i)
                        serious.add(j)
                    # update our abnormal set if the centroid distance is below max distance limit
                    if (D[i, j] < MAX_DISTANCE) and not serious:
                        serious.add(i)
                        serious.add(j)
        # loop over the results
        for (i, (prob, bbox, centroid)) in enumerate(results):
            # extract the bounding box and centroid coordinates, then
            # initialize the color of the annotation
            (startX, startY, endX, endY) = bbox
            (cX, cY) = centroid
            color = (0, 255, 0)
        # if the index pair exists within the vi(grabbed, img) = cap.read()olation/abnormal sets, then update the color
            if i in serious:
                color = (0, 0, 255)
            elif i in abnormal:
                color = (0, 0, 255) #orange = (0, 165, 255)

            # draw (1) a bounding box around the person and (2) the
            # centroid coordinates of the person,
            cv.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            # cv.circle(frame, (cX, cY), 5, color, 2)
        
        # draw some of the parameters
        # Safe_Distance = "Safe distance: >{} px".format(MAX_DISTANCE)
        # cv.putText(frame, Safe_Distance, (470, frame.shape[0] - 25),
        # 	cv.FONT_HERSHEY_SIMPLEX, 0.60, (255, 0, 0), 2)
        # Threshold = "Threshold limit: {}".format(Threshold)
        # cv.putText(frame, Threshold, (470, frame.shape[0] - 50),
        # 	cv.FONT_HERSHEY_SIMPLEX, 0.60, (255, 0, 0), 2)

        # draw the total number of social distancing violations on the output frame
        text = "Counting social distancing violators: {}".format(len(serious))
        cv.putText(frame, text, (10, frame.shape[0] - 55),
            cv.FONT_HERSHEY_SIMPLEX, 0.70, (0, 0, 255), 2)
        
        
        # text1 = "Total abnormal violations: {}".format(len(abnormal))
        # cv.putText(frame, text1, (10, frame.shape[0] - 25),
        # 	cv.FONT_HERSHEY_SIMPLEX, 0.70, (0, 255, 255), 2)
        
        # check to see if the output frame should be displayed to our screen
        # if args["display"] > 0:
            # show the output frame
        video_output.write(frame)
        # cv.imshow("Real-Time Monitoring/Analysis Window", frame)
        # key = cv.waitKey(1) & 0xFF

            # if the `q` key was pressed, break from the loop
        # if key == ord("q"):
                # break
        # update the FPS counter
        fps.update()
        f_c -= 1
        # if an output video file path has been supplied and the video
        # writer has not been initialized, do so now
        # if ["output"] != "" and writer is None:
        # 	# initialize our video writer
        #     fourcc = cv.VideoWriter_fourcc(*"MJPG")
        #     writer = cv.VideoWriter("output", fourcc,25,
        # 		(frame.shape[1], frame.shape[0]))

        # if the video writer is not None, write the frame to the output video file
        # if writer is not None:
    # video_output.write(frame)

    # stop the timer and display FPS information
    fps.stop()
    print("===========================")
    print("[INFO] Elapsed time: {:.2f}".format(fps.elapsed()))
    print("[INFO] Approx. FPS: {:.2f}".format(fps.fps()))

    # close the opened windows
    capture.release()
    video_output.release()
    # cv.destroyAllWindows()

    full_path=f'{current_host}/static/output/{file_name}.avi'
    return {"error": False, "message": "Success", "status_code": 200, "data": {"graph_url" : str(full_path)}}

# print(response_ui)














#     cv.imshow('Output',  frame)
    
    
#     if cv.waitKey(20) & 0xFF ==ord('q'):
#         break
# capture.release()
# cv.destroyAllWindows()