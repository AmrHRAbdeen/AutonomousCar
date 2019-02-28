#!/usr/bin/python
# coding: utf-8


#----------------------------------------------------------------
# Funções: Imagem digital -> Transformação HSV -> Imagem binária -> Erosão binária -> Encontrar área -> Encontrar coordenadas
# Tecnologias: OpenCV, Python e NumPy
#---------------------------------------------------------------

import cv2 as cv2
import time
import numpy as np
#import RPi.GPIO as gpio


def Adjust(area):
    if(area>=1500):
	#car will stop
	print("Red light is on so the car should stop")
    else:
	#car will move
	print("Red light is off So the car is moving ")

#RED
Hmin = 169
Hmax = 189 
Smin = 100
Smax = 255
Vmin = 100
Vmax = 255

rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)

minArea = 50


cv2.namedWindow("Entrada")
cv2.namedWindow("HSV")
cv2.namedWindow("Thre")
cv2.namedWindow("Erosao")


capture = cv2.VideoCapture(0)

width = 250
height = 250

if capture.isOpened():
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  
while True:
    #car is moving
    ret, entrada = capture.read()
    imgHSV = cv2.cvtColor(entrada,cv2.COLOR_BGR2HSV)	
    imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgErode = cv2.erode(imgThresh, None, iterations = 3)
    moments = cv2.moments(imgErode, True)
    area = moments['m00']
    if moments['m00'] >= minArea:
      	 x = moments['m10'] / moments['m00']
       	 y = moments['m01'] / moments['m00']
      	 print(x, ",", y)
         print("area is ",moments['m00'])
         cv2.circle(entrada,(int(x), int(y)), 5, (0, 255, 0), -1)
         Adjust(area) 
	
    cv2.imshow("Entrada",entrada)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("Thre", imgThresh)
    cv2.imshow("Erosao", imgErode)

    if cv2.waitKey(10) == 27:
        break
cv.DestroyAllWindows()
