import cv2

video = cv2.VideoCapture(0)

while 1:
    ret, frame = video.read()
    new_frame = cv2.resize(frame, (500, 300))
    cv2.imshow('video', new_frame)
    key = cv2.waitKey(1)
    if key == 9:
        break


