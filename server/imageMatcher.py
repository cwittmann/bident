import cv2
import geoFilter

# Returns a value showing the certainty of the matching depending on the number of good matches
def getCertainty(goodMatchesCount):
    if goodMatchesCount > 213:
        return "Hoch"
    if goodMatchesCount > 146:
        return "Mittel"
    if goodMatchesCount > 94:
        return "Niedrig"    
    if goodMatchesCount > 0:
        return "Sehr niedrig"   
    
    return None

# Creates and image dictionary which assigns images to their buildings' ids
def createImageDictionary(buildingsInRange):
    imageDictionary = {}

    for building in buildingsInRange:
        buildingId = building.id
        fileName = 'uploads/' + str(buildingId) + '.jpeg'
        imageFile = cv2.imread(fileName, 0)
        imageDictionary.update({buildingId:imageFile})

    return imageDictionary

# Intialize and return the Flann-based Matcher
def initializeFlannMatcher():
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    
    return cv2.FlannBasedMatcher(index_params, search_params)    

# Determines which building in the list is the most likely to match the uploaded image. Feature detection and matching both use the KAZE Features algorithm.
def getBestMatch(allBuildings, userLat, userLng):    
    buildingsInRange = geoFilter.getBuildingsInRange(allBuildings, userLat, userLng)    
    imageDictionary = createImageDictionary(buildingsInRange)
    uploadedImage = cv2.imread('uploads/blob.jpeg', 0)
       
    kaze = cv2.KAZE_create()
    kpUploaded, desUploaded = kaze.detectAndCompute(uploadedImage,None)

    bestMatchSoFar = [0, None]
    flannMatcher = initializeFlannMatcher()

    for imageKey in imageDictionary:
        image = imageDictionary[imageKey]

        kpDB, desDB = kaze.detectAndCompute(image,None)
        matches = flannMatcher.knnMatch(desUploaded,desDB,k=2)

        goodMatchesCount = 0

        for m,n in matches:
            # Lowe's Distance Ratio Test
            if m.distance < 0.7*n.distance:
                goodMatchesCount = goodMatchesCount + 1

        if goodMatchesCount > bestMatchSoFar[0]:
            bestMatchSoFar[0] = goodMatchesCount
            bestMatchSoFar[1] = imageKey

    return bestMatchSoFar[1], getCertainty(goodMatchesCount)
