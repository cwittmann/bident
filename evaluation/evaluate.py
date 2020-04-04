import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import time

def detect(detector, useBinaryDescriptor, imgQuery, imgPathList):   

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flannMatcher = cv2.FlannBasedMatcher(index_params, search_params)   
    bfMatcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)    

    # find the keypoints and descriptors
    kpQuery, desQuery = detector.detectAndCompute(imgQuery,None)       

    for img in imgPathList: 
        
        kpDB, desDB = detector.detectAndCompute(img,None)        

        if (useBinaryDescriptor):
            matches = bfMatcher.knnMatch(desQuery,desDB,k=2)        
        else:
            matches = flannMatcher.knnMatch(desQuery,desDB,k=2)            
        
        goodMatchesCount = 0

        for m,n in matches:
            if m.distance < 0.8*n.distance:
                goodMatchesCount = goodMatchesCount + 1        

        print(str(detector) + " " + str(goodMatchesCount))

def main():
    imgQuery = cv2.imread('evaluation/Testbilder/Bildgroesse/Lorenzkirche100.JPG', 0) # queryImage      
    imgPathList = []   

    imgPathList.append(cv2.imread('evaluation/Testbilder/Bildgroesse/Lorenzkirche50.jpg', 0))
    imgPathList.append(cv2.imread('evaluation/Testbilder/Bildgroesse/Lorenzkirche25.jpg', 0))
    imgPathList.append(cv2.imread('evaluation/Testbilder/Bildgroesse/Lorenzkirche125.jpg', 0))
    imgPathList.append(cv2.imread('evaluation/Testbilder/Bildgroesse/Lorenzkirche6125.jpg', 0))        

    # Initiate detectors
    sift = cv2.xfeatures2d.SIFT_create()
    surf = cv2.xfeatures2d.SURF_create()
    brisk = cv2.BRISK_create()
    orb = cv2.ORB_create()
    kaze = cv2.KAZE_create()
    akaze = cv2.AKAZE_create()    

    startTime = time.time()
    goodMatches = detect(sift, False, imgQuery, imgPathList)
    endTime = time.time()
    print ("SIFT calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" ) 
    
    startTime = time.time()
    goodMatches = detect(surf, False, imgQuery, imgPathList)
    endTime = time.time()
    print ("SURF calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )
    
    startTime = time.time()
    goodMatches = detect(brisk, True, imgQuery, imgPathList)
    endTime = time.time()
    print ("BRISK calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )
   
    startTime = time.time()
    goodMatches = detect(orb, True, imgQuery, imgPathList)
    endTime = time.time()
    print ("ORB calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )

    startTime = time.time()
    goodMatches = detect(kaze, False, imgQuery, imgPathList)
    endTime = time.time()
    print ("KAZE calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )

    startTime = time.time()
    goodMatches = detect(akaze, True, imgQuery, imgPathList)
    endTime = time.time()
    print ("AKAZE calculated " + str(goodMatches) + " good matches in " + str(endTime - startTime) + " seconds" )   ## 

    
main()