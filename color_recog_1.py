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

#green
#Hmin = 42
#Smin = 62
#Vmin = 63
#Hmax = 92
#Smax = 255
#Vmax = 235

#RED
Hmin = 160
Smin = 100
Vmin = 100
Hmax = 179
Smax = 255
Vmax = 255

rangeMin = np.array([Hmin, Smin, Vmin], np.uint8)
rangeMax = np.array([Hmax, Smax, Vmax], np.uint8)

minArea = 50


cv2.namedWindow("Entrada")
cv2.namedWindow("HSV")
cv2.namedWindow("Thre")
cv2.namedWindow("Erosao")


capture = cv2.VideoCapture(0)

# Parametros do tamannho da imagem de captura
width = 250
height = 250

# Definir um tamanho para os frames (descartando o PyramidDown
if capture.isOpened():
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

  
while True:
    ret, entrada = capture.read()
    imgHSV = cv2.cvtColor(entrada,cv2.COLOR_BGR2HSV)	
    imgThresh = cv2.inRange(imgHSV, rangeMin, rangeMax)
    imgErode = cv2.erode(imgThresh, None, iterations = 3)
    moments = cv2.moments(imgErode, True)
    if moments['m00'] >= minArea:
      	 x = moments['m10'] / moments['m00']
       	 y = moments['m01'] / moments['m00']
      	 print(x, ",", y)
         cv2.circle(entrada,(int(x), int(y)), 5, (0, 255, 0), -1)
    
    cv2.imshow("Entrada",entrada)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("Thre", imgThresh)
    cv2.imshow("Erosao", imgErode)

    if cv2.waitKey(10) == 27:
        break
cv.DestroyAllWindows()
