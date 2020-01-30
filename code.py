import numpy as np
import matplotlib.image as mpimg
from PIL import Image
import cv2 as cv

def NivDeGris(image_name): # k est la valeur de seuil entre 0 et 255
    img = Image.open(image_name) # on ouvre l'image
    grisimg = img.convert('L') # conversion en niveau de gris
    grisimg.show()


def open_an_image(image_name):
    img = Image.open(image_name) # on ouvre l'image
    img.show()


def lighting_image(image_name):
    minV, maxV = 240, 255 # intervalle de valeurs pour la "brillance" de la couleur
    image = cv.imread(image_name) # ouverture image ( une nparray )
    image_hsv = cv.cvtColor(image,cv.COLOR_BGR2HSV) # passage en hsv
    ret,seuil = cv.threshold(image_hsv[:,:,2],minV,maxV,cv.THRESH_BINARY)  # seuillage sur la brillance
    cv.imwrite("lighting_image_"+image_name, seuil) # enregistrement image
    
 def filtrage_gaussien(image_name):
    img = cv.imread(image_name)
    h, w, nbc = img.shape
    newImg = cv.GaussianBlur(img, (w-2, h-2), 10)
    cv.imwrite("image_gaussien_"+image_name, newImg)

#lighting_image("mini_cooper_triangle.png")
#lighting_image("mini_cooper_fleche.png")
#open_an_image("mini_cooper_triangle.png")

##################################################################################################
##################################################################################################

# DETECTION DES FORMES

def detecting_edges(image_name):
    image = cv.imread(image_name)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret,thresh = cv.threshold(gray, 240, 255, cv.THRESH_BINARY_INV)
    contours,h = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    shape = "None"
    print("Nombre de contours :",len(contours))
    for cnt in contours:
        perimetre=cv.arcLength(cnt,True)
        approx = cv.approxPolyDP(cnt,0.01*perimetre,True)
        M = cv.moments(cnt)
        cv.drawContours(image,[cnt],-1,(0,255,0),2)
        if len(approx)==3: # on détecte une forme triangulaire
            print("triangle")
        if len(approx)==7:
            print("fleche")


#detecting_edges("mini_cooper_triangle.png")
#detecting_edges("mini_cooper_fleche.png")
