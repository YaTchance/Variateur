import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math

def calculate_color(length):
    #Calculer les composantes de couleur en fonction de la longueur
    color_red_to_blue = (int((1 - length / 255) * 255), 0, int((length / 255) * 255))
    color_blue_to_green = (0, int((1 - length / 255) * 255), int((length / 255) * 255))

    #Combinaison des deux couleurs pour obtenir une variation de couleur complète
    color = (
        color_red_to_blue[0] + color_blue_to_green[0],
        color_red_to_blue[1] + color_blue_to_green[1],
        color_red_to_blue[2] + color_blue_to_green[2]
    )

    return color

def main():
    #Initialisation de la résolution de l'écran et des variables
    wCam, hCam = 1280, 720
    print(f"Résolution de la de l'écran : {wCam}x{hCam}")
    length = 0
    
    #Initialisation du détecteur de mains
    detector = htm.handDetector(detectionCon=0)
    cTime = 0
    pTime = 0
    
    #Initialisation de la capture vidéo
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while True:
        #Lecture de la vidéo et détection des mains
        success, img = cap.read()
        img = detector.findHands(img)
        landmark_list = detector.findPosition(img, draw=False)

        if len(landmark_list):
            #Extraction des points clés pour calculer la longueur
            x1, y1 = landmark_list[4][1], landmark_list[4][2]
            x2, y2 = landmark_list[8][1], landmark_list[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            length = math.hypot(x2 - x1, y2 - y1)

            #Dessin des points et de la ligne entre eux
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)

            #Normalisation de la valeur de la variable "length" de 0-255
            length = int(255 * (length - 40) / (1000 - 40))
            length = max(0, min(255, length))

            print(length)

            try:
                #Calcul de la couleur en fonction de la longueur
                color = calculate_color(length)

                #Dessin du cercle au centre et d'un rectangle en bas de l'écran avec la couleur calculée
                cv2.circle(img, (cx, cy), 10, color, cv2.FILLED)
                cv2.rectangle(img, (50, hCam - int(length)), (100, hCam), color, cv2.FILLED)
            except Exception as e:
                print(f"Erreur de calcul de couleur : {e}")

        #Calcul du FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        #Retournement de l'image
        flipped = cv2.flip(img, 2)

        #Affichage de la barre de graduation avec une couleur variable
        cv2.putText(flipped, f'{int(length)}', (50, hCam - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        #Changement de taille d'écriture FPS
        cv2.putText(flipped, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 100), 2)

        #Affichage de l'image
        cv2.imshow("image", flipped)

        #Quitter la boucle si la touche 'q' est enfoncée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #Libération des ressources et fermeture des fenêtres
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
