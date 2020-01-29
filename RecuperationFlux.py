import cv2 as cv

print(cv.__version__)

vidcap = cv.VideoCapture(0) # 0 pour la webcam
if (vidcap.isOpened() == False):
    print("Error opening video stream or file") #signale si la connexion a échoué
success, image = vidcap.read() #début de la capture
count = 0
while vidcap.isOpened() and count < 100:
    if (count % 10 == 0):
        cv.imwrite("frame%d.jpg" % count, image)  # save frame as jpg file, with the name frameX.jpg with X=count
    success, image = vidcap.read()
    if success:
        cv.imshow('Frame', image) #affiche à l'écran l'image capturée
    if cv.waitKey(25) & 0xFF == ord(' '):
        cv.imwrite("fond.jpg" , image)  # enregistre le nouveau fond en appuyant sur la touche Espace
        print('Nouveau fond')

    if cv.waitKey(25) & 0xFF == ord('q'):
        break # arrete le flux lorsqu'on appuie sur la touche Q

    count += 1

vidcap.release() # deconnexion du flux
cv.destroyAllWindows() #fermeture de toutes les fenêtres
