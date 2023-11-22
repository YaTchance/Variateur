import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm


    
cTime = 0
pTime = 0
cap = cv2.VideoCapture(0)
detector = htm.handDetector()


# Function Start
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img)
    if len(lmlist) !=0 :
        print(lmlist[4], lmlist[8])
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,
              1, (255,0,100),3) #Changement de taille d'écriture FPS
        
    cv2.imshow("img", img)
    cv2.waitKey(1)   