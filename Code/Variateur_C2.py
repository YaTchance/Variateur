import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm

##########################################
wCam, hCam = 1280, 720
##########################################

detector = htm.handDetector(detectionCon=0)
    
cTime = 0
pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
 
# Function Start
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    
    x1, y1 = lmlist[4][1], lmlist[4][2]
    x2, y2 = lmlist[8][1], lmlist[8][2]
    
    cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
    cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
    cv2.line (img, (x1,y1),(x2,y2), (255,0,0), )
    
    if len(lmlist) !=0 :
        print(lmlist[4], lmlist[8])
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,
              1, (255,0,100),3) #Changement de taille d'écriture FPS
    flipped = cv2.flip(img, 1)
    cv2.imshow("image", flipped)    #Inverser le sens de la vidéo
    
    cv2.waitKey(1)  