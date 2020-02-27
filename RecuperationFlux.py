import cv2 as cv

print(cv.__version__)

# vidcap = cv2.VideoCapture('big_buck_bunny_720p_5mb.mp4')
vidcap = cv.VideoCapture(2)  # usb
#vidcap = cv.VideoCapture("http://bs:bs@192.168.43.1:8080/video")  # IP
if (vidcap.isOpened() == False):
    print("Error opening video stream or file")
success, image = vidcap.read()
# cv.imwrite("fond.jpg", image)  # save new background as jpg file
# while (True)
count = 0
while vidcap.isOpened() and count < 1000:
    # if (count % 10 == 0):
    #     cv.imwrite("frame%d.jpg" % count, image)  # save frame as jpg file, with the name frameX.jpg with X=count
    success, image = vidcap.read()
    # if success:
    #     #traiterImage
    #     cv.imshow('Frame', image)
    if cv.waitKey(25) & 0xFF == ord(' '):
        cv.imwrite("fond.jpg" , image)  # save new background as jpg file
        print('Nouveau fond')

    if cv.waitKey(25) & 0xFF == ord('q'):
        break

    count += 1

vidcap.release()
cv.destroyAllWindows()
