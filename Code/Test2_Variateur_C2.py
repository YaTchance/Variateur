import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math
##########################################
wCam, hCam = 1280, 720 #Résolution de l'écran
print(f"Résolution de la de l'écran : {wCam}x{hCam}")
##########################################
length = 0
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
    if len(lmlist):
        x1, y1 = lmlist[4][1], lmlist[4][2]  #Point
        x2, y2 = lmlist[8][1], lmlist[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        
        length = math.hypot(x2 - x1, y2 - y1)
      
        cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
        cv2.line (img, (x1,y1),(x2,y2), (255,0,0),2 )
        
        
########################################################################################################################            
      
    #Normalisation de la valeur de length à la plage 0-255
        length = int(255 * (length - 40) / (1000 - 40))
        length = max(0, min(255, length))  # Assurer que la valeur est entre 0 et 255
        
        print(length)
    #Calculer les composantes de couleur en fonction de la longueur 
   
    try: 
        color_red_to_blue = (int((1 - length / 255) * 255), 0, int((length / 255) * 255))
        color_blue_to_green = (0, int((1 - length / 255) * 255), int((length / 255) * 255))
    
    #Combinaison des deux couleurs pour obtenir une variation de couleur complète
        color = (                                                                                                                    #Cas qu'on ne peut pas gérer, on utilise try/except
        color_red_to_blue[0] + color_blue_to_green[0],  
        color_red_to_blue[1] + color_blue_to_green[1],
        color_red_to_blue[2] + color_blue_to_green[2]
            )
        cv2.circle(img, (cx,cy),10, (color), cv2.FILLED)
        cv2.rectangle(img, (50, hCam - int(length)), (100, hCam), color, cv2.FILLED)
    except: 
            pass
        
########################################################################################################################        
    #Calculer le FPS en temps réel
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    
########################################################################################################################        
    #Inverser le sens de la vidéo
    flipped = cv2.flip(img, 2)
    
    # Affichage de la barre de graduation avec une couleur variable
    cv2.putText(flipped, f'{int(length)}', (50, hCam - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
    
    #Changement de taille d'écriture FPS
    cv2.putText(flipped, f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,100),2) 
    
    
    cv2.imshow("image", flipped)    
    
######################################################################################################################## 

    if cv2.waitKey(1) & 0xFF == ord('q'): #Pour Quitter la programmation test , appuyer sur "q"
        break
cap.release()
cv2.destroyAllWindows()
########################################################################################################################    