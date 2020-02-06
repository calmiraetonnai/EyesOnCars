from code import Image_Treatment
import cv2 as cv
import numpy as np
import pytesseract
from PIL import Image

#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR"
# pytesseract.image_to_osd(Image.open('test.png'))) orientation + script descrption
#https://www.youtube.com/watch?v=Fchzk1lDt7Q

def stackImages(scale, imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv.cvtColor( imgArray[x][y], cv.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv.cvtColor(imgArray[x], cv.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver # permet un affichage complet de la liste d'image donnée en paramètre

def test(nom_de_voiture):
    IMG = Image_Treatment("fond.jpg") # initialisation
    IMG.get_state(nom_de_voiture) # attribution d'un etat
    IMG.processed.append(IMG.current_state) # 1er process
    IMG.current_state = cv.cvtColor(IMG.current_state,cv.COLOR_BGR2GRAY) # gray
    seuil, img_seuil = cv.threshold(IMG.current_state, 230, 255, cv.THRESH_BINARY) # seuillage
    IMG.processed.append(img_seuil) # 2e process
    contours, _ = cv.findContours(img_seuil, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) # contours

    kernel = np.ones((5, 5), np.uint8)
    img = cv.imread(nom_de_voiture) # copie de l'image de base pour placer centres et rectangles
    stack_detection = [] # Ensemlble des motifs détectés
    for cnt in contours: # pour chaque contour
        (x, y, w, h) = cv.boundingRect(cnt)  # on fait un rectangle
        if (h >= 100) & (w < 500) & (h < 300) & (w>=200): # environ la taille des formes à obtenir
            M = cv.moments(cnt)
            if (M["m00"]!=0):
                # recuperation du centre de masse
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv.putText(img, "X", (cX,cY), cv.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),3) # texte sur l'image

            img_crop = img_seuil[y:y + h, x:x + w]
            img_resize = cv.resize(img_crop, (0, 0), fx=5, fy=5)
            img_corrige = cv.morphologyEx(img_resize, cv.MORPH_OPEN, kernel)
            stack_detection.append([img_corrige]) # motif reconnu
            cv.rectangle(img, (x,y), (x+w, y+h), (0,255,0),5)

    IMG.processed.append(img) # 3e process avec reco

    # formes reconnues
    stack_detection = stackImages(0.3, stack_detection) # création de l'image stackée
    cv.imwrite("stack_detection.jpg", stack_detection) # enregistrement
    cv.imshow("J'ai reconnu les formes suivantes... :", stack_detection) # affichage utilisateur
    cv.waitKey(0)

    # evolution des traitements
    stack = stackImages(0.15, [IMG.processed]) # création de l'image stackée
    cv.imwrite("processing.jpg", stack) # enregistrement
    cv.imshow("Evolution des traitements realises", stack) # affichage utilisateur
    cv.waitKey(0)

# Test sur chaque voiture
test("voit_h.jpg")
test("voit_8.jpg")
