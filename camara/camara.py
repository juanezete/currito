from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time
import numpy as np
import imutils
import serial


defaultSpeed = 80
windowCenter = 320
centerBuffer = 10
pwmBound = float(50)
cameraBound = float(320)
kp = (pwmBound / cameraBound)*1.4
leftBound = int(windowCenter - centerBuffer)
rightBound = int(windowCenter + centerBuffer)
error = 0
ballPixel = 0

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def enviar_dato(dato1, dato2, dato3):
        # Lee la entrada del usuario
        dato1 = int(dato1)
        dato2 = int(dato2)
        dato3 = int(dato3)
        data = f"{dato2},{dato1}, {dato3} \n"
                
        ser.write(data.encode())
        print(data.encode())
        time.sleep(0.1)     
       


def pwmStop():
#cambiar print
    enviar_dato(0,0,0)

#Camera setup
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size = (640, 480))

time.sleep(0.1)

lower_yellow = np.array([13, 50, 0])
upper_yellow = np.array([30, 255, 255])

camera.capture_continuous(rawCapture, format="bgr", use_video_port=True)


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    output = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    output = cv2.bitwise_and(output, output, mask=mask)
    #output = cv2.dilate(output, None, iterations=2)
    #output = cv2.erode(output, None, iterations=2)
    gray = cv2.cvtColor(output, cv2.COLOR_BGR2GRAY)
    #_, binary = cv2.threshold(gray, 1, 255, cv2. THRESH_BINARY)
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 3, 500, minRadius = 10, maxRadius = 200, param1 = 100,  param2 = 60)
    #cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    ballPixel = 0

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, radius) in circles:

            cv2.circle(output, (x, y), radius, (0, 255, 0), 4)
        #cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)	

            if radius > 10:
                ballPixel = x
            else:
                ballPixel = 0

    cv2.imshow("output", output)
    key = cv2.waitKey(1) & 0xFF
    rawCapture.truncate(0)

    #Proportional controller
    if ballPixel == 0:
        #print "no ball"
        error = 0
        pwmStop()
    elif (ballPixel < leftBound) or (ballPixel > rightBound):
        error = windowCenter - ballPixel
        pwmOut = abs(error * kp) 
        #print ballPixel
        turnPwm = pwmOut + defaultSpeed
        if  ballPixel < (leftBound):
            #print "left side"
            if radius > 50 and ballPixel < 110:
                print (ballPixel)
                print("derecha 1")
                enviar_dato(defaultSpeed*1.5,defaultSpeed - 30, 0)
            else:
                print("derecha 2")
                enviar_dato(turnPwm*1.5, defaultSpeed, 0)
        elif ballPixel > (rightBound):
            #print "right side"
            if radius > 50 and ballPixel > 540:
                print("izquierda 1")
                print (ballPixel)
                enviar_dato(defaultSpeed - 30, defaultSpeed, 0)
            else:
                print("izquierda 2")
                enviar_dato(defaultSpeed, turnPwm, 0)
        else:
        #print "middle"
            print("medio")
            if (radius < 40):
                print("en medio")
                enviar_dato(defaultSpeed, defaultSpeed, 0)
            else:
                pwmStop()

    if key == ord('q'):
        break
    
    time.sleep(0.8)

cv2.destroyAllWindows()
camera.close()
pwmStop()
GPIO.cleanup()
