import numpy as np
import cv2
import apriltag

def init_camera():
    #video_capture = cv2.VideoCapture(CAMERA_INDEX)
    video_capture = cv2.VideoCapture("../Downloads/apriltag-pad.jpg")

    if not video_capture.isOpened():
        print("error when opening camera video_captureture")
        exit()

    frame_width = video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print ("camera resolution {}x{}".format(frame_width, frame_height))

    return video_capture

def find_extreme_tags (tags):

    if not tags or len(tags) < 4:
        return None, None, None, None

    tag_right = max(tags, key=lambda t: t.center[0])
    tag_left = min(tags, key=lambda t: t.center[0])
    tag_top = min(tags, key=lambda t: t.center[1])
    tag_bottom = max(tags, key=lambda t: t.center[1])

    return tag_right, tag_left, tag_top, tag_bottom

def mark_tags_on_screen (frame, tags):
    extreme_tags = find_extreme_tags(tags)

    if not extreme_tags:
        pass #TODO

    extreme_color = (0,0,255)
    regular_color = (0,255,0)


    for tag in tags:
        if tag in extreme_tags:
            color = extreme_color
        else:
            color = regular_color
        cv2.line (frame, tuple(map(int,tag.corners[0])), tuple(map(int,tag.corners[1])), color, thickness=2) 
        cv2.line (frame, tuple(map(int,tag.corners[1])), tuple(map(int,tag.corners[2])), color, thickness=2) 
        cv2.line (frame, tuple(map(int,tag.corners[2])), tuple(map(int,tag.corners[3])), color, thickness=2) 
        cv2.line (frame, tuple(map(int,tag.corners[3])), tuple(map(int,tag.corners[0])), color, thickness=2) 

        cv2.putText(frame, str(tag.tag_id), (int(tag.center[0]), int(tag.center[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

def main():
    CAMERA_INDEX = 0

    tag_size_in_meters = 0.1

    detector_options = apriltag.DetectorOptions(families="tag36h11")
    tag_detector = apriltag.Detector(detector_options)

    video_capture = init_camera()
    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("error, not able to read frame")
            video_capture.release()
            exit()

        frame = cv2.resize(frame, (640,480))
    #    frame = cv2.resize(frame, (800,600))
        grayFrame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        tags =tag_detector.detect(grayFrame)

        mark_tags_on_screen(frame, tags)
        cv2.imshow("kaka", frame)

        if cv2.waitKey(0) == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
