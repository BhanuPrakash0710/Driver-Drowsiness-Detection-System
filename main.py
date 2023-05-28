#Required Libraries
import cv2
import dlib
import numpy as np
from imutils import face_utils
import serial

#To Establish Serial communication with Arduino
Serial_Com = serial.Serial('COM3',9600)

#Video stream input
cap = cv2.VideoCapture(0)

#Face detection
detector = dlib.get_frontal_face_detector()

#Landmarks generation
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

sleep = 0
active = 0
status =""
color = (0,0,0)

#Euclidian distance function
def compute(ptA,ptB):
    dist = np.linalg.norm(ptA - ptB)
    return dist

#EAR algorithm
def blinked(a,b,c,d,e,f):
    up = compute(b,d) + compute(c,e)
    down = compute(a,f)
    ratio = up/(2.0*down)

    if(ratio>0.2):
        return 2
    else:
        return 0

while True:
    _,img = cap.read()
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = detector(imgGray)

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()

        face_frame = img.copy()
        cv2.rectangle(face_frame,(x1,y1),(x2,y2),(0,255,0),2)

        landmarks = predictor(imgGray,face)
        landmarks = face_utils.shape_to_np(landmarks)

        left_blink = blinked(landmarks[36],landmarks[37],landmarks[38],landmarks[41],landmarks[40],landmarks[39])

        right_blink = blinked(landmarks[42],landmarks[43],landmarks[44],landmarks[47],landmarks[46],landmarks[45])

        if(left_blink==0 or right_blink==0):
            sleep = sleep+1
            active = 0
            if(sleep>6):
                Serial_Com.write(b'a')
                status = "Drowsy!!!"
                color = (0, 0, 255)
            
        else:
            sleep = 0
            active = active+1
            if(active>6):
                Serial_Com.write(b'b')
                status = "Active :)"
                color = (0,255,0)

        cv2.putText(img,status,(100,100),cv2.FONT_HERSHEY_SIMPLEX,1.2,color,3)

        for n in range(0,68):
            (x,y) = landmarks[n]
            cv2.circle(img,(x,y),1,(255,255,255),-1)

    cv2.imshow("VedioStream",img)
    #cv2.imshow("Result of detector",face_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


        




