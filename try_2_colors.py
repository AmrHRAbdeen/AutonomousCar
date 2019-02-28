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
G_Hmin = 42
G_Smin = 62
G_Vmin = 63
G_Hmax = 92
G_Smax = 255
G_Vmax = 235

G_rangeMin = np.array([G_Hmin,G_Smin,G_Vmin], np.uint8)
G_rangeMax = np.array([G_Hmax,G_Smax,G_Vmax], np.uint8)

#RED
R_Hmin = 160
R_Smin = 100
R_Vmin = 100
R_Hmax = 179
R_Smax = 255
R_Vmax = 255

R_rangeMin = np.array([R_Hmin,R_Smin,R_Vmin], np.uint8)
R_rangeMax = np.array([R_Hmax,R_Smax,R_Vmax], np.uint8)

minArea = 50

cv2.namedWindow("Entrada")
cv2.namedWindow("HSV")
cv2.namedWindow("Green_Thre")
cv2.namedWindow("Red_Thre")
cv2.namedWindow("Green_Erosao")
cv2.namedWindow("Red_Erosao")


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
    G_imgThresh = cv2.inRange(imgHSV,G_rangeMin,G_rangeMax)
    R_imgThresh = cv2.inRange(imgHSV,R_rangeMin,R_rangeMax)
    
    G_imgErode = cv2.erode(G_imgThresh, None, iterations = 3)
    R_imgErode = cv2.erode(R_imgThresh, None, iterations = 3)
    
    G_moments = cv2.moments(G_imgErode, True)
    R_moments = cv2.moments(R_imgErode, True)
    
    if G_moments['m00'] >= minArea:
      	 x = G_moments['m10'] / G_moments['m00']
       	 y = G_moments['m01'] / G_moments['m00']
      	 print("Green Pos:",x, ",", y)
         cv2.circle(entrada,(int(x), int(y)), 5, (0, 255, 0), -1)

    if R_moments['m00'] >= minArea:
      	 x = R_moments['m10'] / R_moments['m00']
       	 y = R_moments['m01'] / R_moments['m00']
      	 print("Red Pos:",x, ",", y)
         cv2.circle(entrada,(int(x), int(y)), 5, (0,0,255), -1)
    
    cv2.imshow("Entrada",entrada)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("Green_Thre", G_imgThresh)
    cv2.imshow("Green_Erosao", G_imgErode)
    cv2.imshow("Red_Thre", R_imgThresh)
    cv2.imshow("Red_Erosao",R_imgErode)

    if cv2.waitKey(10) == 27:
        break
cv.DestroyAllWindows()
