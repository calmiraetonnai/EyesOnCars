import numpy as np
import cv2 as cv
import pyzbar.pyzbar as pyzbar

class Image_Treatment():

    def __init__(self, bg):
        self.background = cv.imread(bg) # ouverture image ( une nparray )
        self.current_state = None # Initialisation du fond
        self.original_state = None
        self.processed = []

    def reset(self):
        self.current_state = self.original_state # on reinitialise tout les traitements faits

    def get_state(self, image_name): # OK
        """ Attribut une image ( équivalent de l'etat courant du systeme ) """
        self.current_state = cv.imread(image_name)
        self.original_state = cv.imread(image_name)

    def substract_background(self):
        """ soustraction de fond """
        substract = abs(self.background - self.current_state) #soustraction de fond
        new_name = "soustraction.jpg"
        cv.imwrite(new_name, substract) # enregistrement
        self.current_state = substract # association
        #self.processed.append(substract)

    def filtering(self, methode): # OK mais à appliquer sur une image bruité
        """ Filtrage Median ou Moyen ou Gaussien """
        # methode = 0 pour Filtrage moyen
        # methode = 1 pour Filtrage median
        # methode = 2 pour Filtrage gaussien
        if methode == 1:
            new = cv.medianBlur(self.current_state,5) # Filtre Median
        elif methode == 2:
            new = cv.GaussianBlur(self.current_state, (9, 9), cv.BORDER_DEFAULT) # Filtre Gaussien
        else:
            new = cv.blur(self.current_state,(5,5)) # Filtre Moyen
        new_name = "filtrage.jpg"
        cv.imwrite(new_name, new) # enregistrement
        self.processed.append(new)

    def lighting_image(self, m, M):  # a tester sur les valeurs de m et M
        """ Traitement de l'intensité de lumière sur l'image + Seuillage """
        minV, maxV = m, M # intervalle de valeurs pour la "brillance" de la couleur
        image_hsv = cv.cvtColor(self.current_state,cv.COLOR_BGR2HSV) # passage en hsv
        ret,seuil = cv.threshold(image_hsv[:,:,2],minV,maxV,cv.THRESH_BINARY)  # seuillage sur la brillance
        self.current_state = seuil
        new_name = "luminance.jpg"
        cv.imwrite(new_name, seuil) # enregistrement image
        #self.processed.append(self.current_state)

    def match_de_template(self):
        template = cv.imread(self.templates[0])
        result = cv.matchTemplate(self.current_state, template, cv.TM_SQDIFF_NORMED)
        position_of_template = (255 * result / result.max()).astype(np.uint8)
        cv.imwrite("position_template.jpg", position_of_template) # NON TESTABLE

    def Sobel_filter(self): # VRAIMENT PAS BON

        ddepth = cv.CV_16S
        blur = cv.GaussianBlur(self.current_state, (3, 3), 0)

        grad_x = cv.Sobel(blur, ddepth, 1, 0, ksize=3, scale=0, delta=1, borderType=cv.BORDER_DEFAULT)
        grad_y = cv.Sobel(blur, ddepth, 0, 1, ksize=3, scale=0, delta=1, borderType=cv.BORDER_DEFAULT)

        abs_grad_x = cv.convertScaleAbs(grad_x)
        abs_grad_y = cv.convertScaleAbs(grad_y)

        sobel = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        cv.imwrite("sobel.jpg", sobel)

    def canny_processing(self, th1, th2):
        canny = cv.Canny(self.current_state, th1, th2)
        cv.imwrite("canny.jpg", canny)
        self.processed.append(canny)

    def detecting_edges(self): # NE MARCHE PAS ENCORE BIEN
        copie = cv.bitwise_not(self.current_state)
        ret,thresh = cv.threshold(copie, 240, 255, cv.THRESH_BINARY_INV)
        contours,h = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        shape = "None"
        print("Nombre de contours :",len(contours))
        for cnt in contours:
            perimetre = cv.arcLength(cnt,True)
            approx = cv.approxPolyDP(cnt,0.1*perimetre,True)
            #print("Nb contours de la forme :", len(approx))

            M = cv.moments(cnt)
            if (M["m00"]!=0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                cv.drawContours(copie,[cnt],-1,(255,0,0),2)
                if len(approx)==3: # on détecte une forme triangulaire
                    shape = "triangle"
                    print("triangle")
                if len(approx)==7:
                    shape = "fleche"
                    print("fleche")

                cv.putText(copie, shape, (cX, cY), cv.FONT_HERSHEY_SIMPLEX,0.5, (255, 255, 255), 2)

        cv.imwrite('copie.jpg',copie)
     
    def Qrcode(self):
        Codes = pyzbar.decode(self.current_state)#liste contentant les differents codes
        #traitement pour chaque code
        for code in Codes:
            points = code.polygon #liste des points des quatres coins du code
            data = code.data.decode("utf-8") #data données sur code, data.type pour type du code (QRCODE ou Code barre)

            #lignes suivantes sert aux inscriptions sur l'image
            pt1 = (min(points[0][0], points[2][0]), min(points[0][1], points[2][1])) #coordonnées coins sup gauche
            pt2 = (max(points[0][0], points[2][0]), max(points[0][1], points[2][1])) #coordonnées coins inf droit
            cv.rectangle(self.current_state, pt1, pt2, (0, 0, 255), 3) #encadre le qr code
            cv.putText(self.current_state, data, (pt1[0], pt2[1] + 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        

