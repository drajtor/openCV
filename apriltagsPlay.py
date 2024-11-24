import numpy as np
import cv2
import apriltag

CAMERA_INDEX = 0

tag_size_in_meters = 0.1

detector_options = apriltag.DetectorOptions(families="tag36h11")
tag_detector = apriltag.Detector(detector_options)

video_capture = cv2.VideoCapture(CAMERA_INDEX)
#video_capture = cv2.VideoCapture("../Downloads/apriltag-pad.jpg")

if not video_capture.isOpened():
    print("error when opening camera video_captureture")
    exit()

frame_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
print ("camera resolution {}x{}".format(frame_width, frame_height))

camera_matrix = np.array([[600,0,frame_width/2],
                          [0,600,frame_height/2],
                          [0,0,1]])

camera_parameters = camera_matrix[0,0], camera_matrix[1,1], camera_matrix[0,2], camera_matrix[1,2]

while True:
    ret, frame = video_capture.read()

    if not ret:
        print("error, not able to read frame")
        video_capture.release()
        exit()

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    tags =tag_detector.detect(grayFrame)

#    print ("detected tags: {}".format(len(tags)))


    for tag in tags:
        pose, e0, e1 = tag_detector.detection_pose(tag, camera_parameters, tag_size_in_meters)
        cv2.line (frame, tuple(map(int,tag.corners[0])), tuple(map(int,tag.corners[1])), (0,255,0), thickness=2) 
        cv2.line (frame, tuple(map(int,tag.corners[1])), tuple(map(int,tag.corners[2])), (0,255,0), thickness=2) 
        cv2.line (frame, tuple(map(int,tag.corners[2])), tuple(map(int,tag.corners[3])), (0,255,0), thickness=2) 
        cv2.line (frame, tuple(map(int,tag.corners[3])), tuple(map(int,tag.corners[0])), (0,255,0), thickness=2) 


    cv2.imshow("kaka", frame)
    #cv2.imshow("kaka", grayFrame) 

    if cv2.waitKey(1) == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
