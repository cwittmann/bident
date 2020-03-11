import cv2
import geoFilter
from flask import jsonify

def getBestMatch(allBuildings, userLat, userLng):

    buildingsInRange = geoFilter.getBuildingsInRange(allBuildings, userLat, userLng)    

    imgDictionary = {}

    for building in buildingsInRange:
        buildingId = building.id
        fileName = 'uploads/' + str(buildingId) + '.jpeg'
        imgFile = cv2.imread(fileName, 0)
        imgDictionary.update({buildingId:imgFile})

    imgQuery = cv2.imread('uploads/blob.jpeg', 0) # queryImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # find the keypoints and descriptors with SIFT
    kpQuery, desQuery = sift.detectAndCompute(imgQuery,None)

    bestMatch = [0, None]

    for imgKey in imgDictionary:
        img = imgDictionary[imgKey]

        kpDB, desDB = sift.detectAndCompute(img,None)
        matches = flann.knnMatch(desQuery,desDB,k=2)

        goodMatchesCount = 0

        for m,n in matches:
            if m.distance < 0.7*n.distance:
                goodMatchesCount = goodMatchesCount + 1

        if goodMatchesCount > bestMatch[0]:
            bestMatch[0] = goodMatchesCount
            bestMatch[1] = imgKey

    return bestMatch[1], "99.9"