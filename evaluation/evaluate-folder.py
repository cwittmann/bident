import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os
import time

def detect(detector, useBinaryDescriptor, imgPathList, goodMatchesArray):   

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flannMatcher = cv2.FlannBasedMatcher(index_params, search_params)   
    bfMatcher = cv2.DescriptorMatcher_create(cv2.DescriptorMatcher_BRUTEFORCE_HAMMING)       

    imgQuery1 = cv2.imread('evaluation/test-images/Oxford/Brauttor.JPG', 0)
    imgQuery2 = cv2.imread('evaluation/test-images/Oxford/Lorenzkirche.JPG', 0)
    imgQuery3 = cv2.imread('evaluation/test-images/Oxford/Schuerstabhaus.JPG', 0)

    kpQuery1, desQuery1 = detector.detectAndCompute(imgQuery1,None)       
    kpQuery2, desQuery2 = detector.detectAndCompute(imgQuery2,None)       
    kpQuery3, desQuery3 = detector.detectAndCompute(imgQuery3,None)       

    counter = 0

    for imgPath in imgPathList:          

        counter = counter + 1   

        # The following images can cause unexplained errors with some algorithms
        if "trinity_000122.jpg" in imgPath or "new_000453.jpg" in imgPath:           
            continue   

        if counter % 50 != 1:
            continue

        img = cv2.imread(imgPath, 0)        

        kpDB, desDB = detector.detectAndCompute(img,None)        

        allMatches = []

        if (useBinaryDescriptor):
            allMatches.append(bfMatcher.knnMatch(desQuery1,desDB,k=2))        
            allMatches.append(bfMatcher.knnMatch(desQuery2,desDB,k=2))        
            allMatches.append(bfMatcher.knnMatch(desQuery3,desDB,k=2))        
        else:
            allMatches.append(flannMatcher.knnMatch(desQuery1,desDB,k=2))            
            allMatches.append(flannMatcher.knnMatch(desQuery2,desDB,k=2)) 
            allMatches.append(flannMatcher.knnMatch(desQuery3,desDB,k=2)) 
        
        for matches in allMatches:

            goodMatchesCount = 0

            for m,n in matches:
                if m.distance < 0.8*n.distance:
                    goodMatchesCount = goodMatchesCount + 1

            print(str(imgPath) + ": " + str(goodMatchesCount) + " good matches.")

            goodMatchesArray.append(goodMatchesCount)         
    
    return goodMatchesArray
   

def getImagesFromDirectory():

    # To compare with buildings from Oxford Buildings Dataset, please download it from https://www.robots.ox.ac.uk/~vgg/data/oxbuildings/ and extract
    # its contents to the folder specified in the filesPath variable.
    filesPath = 'evaluation/test-images/Oxford/Oxford Buildings Dataset/'
    files = os.listdir(filesPath)
    
    imgPathList = []

    counter = 0

    for file in files:

        filePath = os.path.abspath(os.path.join(filesPath, file))               
        imgPathList.append(filePath)
        counter = counter + 1        
    
    return imgPathList

def main():
    
    imgPathList = []   
    imgPathList = getImagesFromDirectory()   

    sift = cv2.xfeatures2d.SIFT_create()
    surf = cv2.xfeatures2d.SURF_create()
    brisk = cv2.BRISK_create()
    orb = cv2.ORB_create()
    kaze = cv2.KAZE_create()
    akaze = cv2.AKAZE_create()    

    siftMatches = []
    startTime = time.time()
    goodMatches = detect(sift, False, imgPathList, siftMatches)
    endTime = time.time()
    print ("SIFT calculated the following good matches " + str(goodMatches) + " in " + str(endTime - startTime) + " seconds" )  
       
    surfMatches = []
    startTime = time.time()
    goodMatches = detect(surf, False, imgPathList, surfMatches)
    endTime = time.time()
    print ("SURF calculated the following good matches " + str(goodMatches) + " in " + str(endTime - startTime) + " seconds" )  

    briskMatches = []
    startTime = time.time()
    goodMatches = detect(brisk, True, imgPathList, briskMatches)
    endTime = time.time()
    print ("BRISK calculated the following good matches " + str(goodMatches) + " in " + str(endTime - startTime) + " seconds" )  

    orbMatches = []
    startTime = time.time()
    goodMatches = detect(orb, True, imgPathList, orbMatches)
    endTime = time.time()
    print ("ORB calculated the following good matches " + str(goodMatches) + " in " + str(endTime - startTime) + " seconds" )  

    kazeMatches = []
    startTime = time.time()
    goodMatches = detect(kaze, False, imgPathList, kazeMatches)
    endTime = time.time()
    print ("KAZE calculated the following good matches " + str(goodMatches) + " in " + str(endTime - startTime) + " seconds" )  

    akazeMatches = []
    startTime = time.time()
    goodMatches = detect(akaze, True, imgPathList, akazeMatches)
    endTime = time.time()
    print ("AKAZE calculated the following good matches " + str(goodMatches) + " in " + str(endTime - startTime) + " seconds" )  

    matchesArray = []
    matchesArray.append(siftMatches)
    matchesArray.append(surfMatches)
    matchesArray.append(briskMatches)
    matchesArray.append(orbMatches)
    matchesArray.append(kazeMatches)
    matchesArray.append(akazeMatches)

    # Calculate Percentiles
    siftPercentiles = np.percentile(siftMatches, [0, 10, 50, 90, 100])
    print(siftPercentiles)
    surfPercentiles = np.percentile(surfMatches, [0, 10, 50, 90, 100])
    print(surfPercentiles)
    briskPercentiles = np.percentile(briskMatches, [0, 10, 50, 90, 100])
    print(briskPercentiles)
    orbPercentiles = np.percentile(orbMatches, [0, 10, 50, 90, 100])
    print(orbPercentiles)
    kazePercentiles = np.percentile(kazeMatches, [0, 10, 50, 90, 100])
    print(kazePercentiles)
    akazePercentiles = np.percentile(akazeMatches, [0, 10, 50, 90, 100])
    print(akazePercentiles)

    # Draw boxplot and save in file    
    mpl.use('agg')
    fig = plt.figure(1, figsize=(9, 12))
    ax = fig.add_subplot(111)
    bp = ax.boxplot(matchesArray, patch_artist=True)    

    for box in bp['boxes']:    
        box.set( color='#7570b3', linewidth=2)    
        box.set( facecolor = '#1b9e77' )

    for whisker in bp['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)

    for cap in bp['caps']:
        cap.set(color='#7570b3', linewidth=2)


    for median in bp['medians']:
        median.set(color='#b2df8a', linewidth=2)
    
    for flier in bp['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5)

    ax.set_xticklabels(['SIFT', 'SURF', 'BRISK', 'ORB', 'KAZE', 'AKAZE'])
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    ax.set_xlabel('Algorithmus')
    ax.set_ylabel('Anzahl guter Matches')

    fig.savefig('evaluation/fig1.png', bbox_inches='tight')


main()