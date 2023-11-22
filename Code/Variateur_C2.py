import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
##########################################
wCam, hCam = 1280, 720 #Résolution de l'écran
print(f"Résolution de la de l'écran : {wCam}x{hCam}")
##########################################

detector = htm.handDetector(detectionCon=0)
cTime = 0
pTime = 0
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

########################################################################################################################    
# Function Start
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
########################################################################################################################    
    if (len(lmlist)):
        x1, y1 = lmlist[4][1], lmlist[4][2]
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1+x2) // 2, (y1+y2)//2
        
        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line (img, (x1,y1),(x2,y2), (255,0,0),2 )
        cv2.circle(img, (cx,cy),10, (255,0,255), cv2.FILLED)
########################################################################################################################            
        length = math.hypot(x2-x1, y2-y1)
        print(length)
        # Normalisation de la valeur de length à la plage 0-255
        length = int(255 * (length - 40) / (1000 - 40))
        length = max(0, min(255, length))  # Assurer que la valeur est entre 0 et 255

        # Interpolation linéaire entre vert (0, 255, 0) et bleu(255, 0, 0)
        color = (int((1 - length / 255) * 255), int((length / 255) * 255), 0)

        cv2.circle(img, (cx, cy), 10, color, cv2.FILLED)
        #Afficher la barre graduer
    cv2.rectangle(img, (50, hCam - int(length)), (100, hCam), color, cv2.FILLED)
    cv2.putText(img, f'{int(length)}', (50, hCam - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
########################################################################################################################        
  
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
########################################################################################################################        
   
    flipped = cv2.flip(img, 2)
    
    cv2.putText(flipped, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,
              1, (255,0,100),2) #Changement de taille d'écriture FPS
    cv2.imshow("image", flipped)    #Inverser le sens de la vidéo
    
########################################################################################################################    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
########################################################################################################################    