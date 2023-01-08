import cv2

#############################################
frameWidth = 1900
frameHeight = 1200
frontalFaceCascade = cv2.CascadeClassifier("C:\\Users\\kanat\\Documents\\python\\haarcascades\\haarcascade_frontalface_default.xml")
Nose = cv2.CascadeClassifier("C:\\Users\\kanat\\Documents\\python\\haarcascades\\cars.xml")
minArea = 200
color = (255, 0, 255)
colour = (0, 255, 255)
colcour = (0, 0, 255)
###############################################
cap = cv2.VideoCapture(0)
cap.set(3,  frameWidth)
cap.set(4,  frameHeight)
cap.set(10, 150)
count = 0

while True:
    success,  img = cap.read()
    imgGray = cv2.cvtColor(img,  cv2.COLOR_BGR2GRAY)
    face = frontalFaceCascade.detectMultiScale(imgGray,  1.1,  10, cv2.CASCADE_FIND_BIGGEST_OBJECT)
    nose = Nose.detectMultiScale(imgGray,  1.1,  10, cv2.CASCADE_FIND_BIGGEST_OBJECT)
    for (x,  y,  w,  h) in face:
        area = w*h
        if area > minArea:
            cv2.rectangle(img,  (x,  y),  (x + w,  y + h),  (255,  0,  255),  2)
            cv2.putText(img, "Face", (x, y-5),  cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, color, 2)
            imgRoi = img[y:y+h, x:x+w]
            cv2.imshow("Result",  img)
            if cv2.waitKey(1) and 0xFF == ord('s'):
                cv2.imwrite("Resources/Scanned/NoPlate_"+str(count)+".jpg", imgRoi)
                cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX,  2, (0, 0, 255), 2)
                cv2.imshow("Result", img)
                cv2.waitKey(500)
                count += 1
    for (x,  y,  w,  h) in nose:
        area = w*h
        if area > minArea:
            cv2.rectangle(img,  (x,  y),  (x + w,  y + h),  colcour,  2)
            cv2.putText(img, "Car", (x, y-5),  cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, colcour, 2)
            imgRoi = img[y:y+h, x:x+w]

            cv2.imshow("Result",  img)
            if cv2.waitKey(1) and 0xFF == ord('s'):
                cv2.imwrite("Resources/Scanned/NoPleate_"+str(count)+".jpg", imgRoi)
                cv2.rectangle(img, (0, 200), (640, 300), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, "Scan Saved", (150, 265), cv2.FONT_HERSHEY_DUPLEX,  2, (0, 0, 255), 2)
                cv2.imshow("Result", img)
                cv2.waitKey(500)
                count += 1
