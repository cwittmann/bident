import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
cors = CORS(app)

def getBestMatch():

    jsonDataFile = open("data/data.json")
    data = json.load(jsonDataFile)

    imgList = []

    for dataObject in data:
        objectId = dataObject["id"]
        filename = 'images/' + str(objectId) + '.jpg'
        imgFile = cv2.imread(filename, 0)        
        imgList.append(imgFile)

    imgQuery = cv2.imread('uploads/blob.jpeg', 0) # queryImage  

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # find the keypoints and descriptors with SIFT
    kpQuery, desQuery = sift.detectAndCompute(imgQuery,None)    

    goodMatches = []

    for img in imgList:
        kpDB, desDB = sift.detectAndCompute(img,None)        
        matches = flann.knnMatch(desQuery,desDB,k=2)
        
        goodMatchesCount = 0

        for m,n in matches:
            if m.distance < 0.7*n.distance:
                goodMatchesCount = goodMatchesCount + 1
        
        goodMatches.append(goodMatchesCount)  
  
    indexOfBestMatch = goodMatches.index(max(goodMatches))

    bestMatch = data[indexOfBestMatch]

    return bestMatch["id"], "99.9"
    

def createResult():
    
    bestMatchId, bestMatchCertainty = getBestMatch()
    
    return jsonify(
        id=bestMatchId,
        certainty=bestMatchCertainty
    )

@app.route('/', methods = ['GET', 'POST'])
def returnResult():
    if request.method == 'POST':
        print('=== UPLOAD ATTEMPTED ===')
        
        if request.files == None:
            print("NO FILES")

        file = request.files['canvasImage']        

        if file is None:
            print('=== NO FILE NAMED FILE ===')
            return "ERROR: NO FILE NAMED FILE"        
        
        if file.filename == '':
            print('=== NO SELECTED FILE ===')
            return "ERROR: FILENAME IS EMPTY"
        if file:
            print('=== FILE FOUND ===')            
            file.save('./uploads/blob.jpeg')
            print('=== FILE SUCCESSFULLY UPLOADED ===')                      
            return createResult()

app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

# curl -F "file=@image.jpg" http://localhost:8000/home