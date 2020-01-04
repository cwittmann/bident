import cv2
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

def calculateQuality():
    img1 = cv2.imread('uploads/blob.jpeg', 0) # queryImage    
    img2 = cv2.imread('images/tyn2.png', 0) # trainImage

    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=2)

    # store all the good matches as per Lowe's ratio test.
    good = []
    for m,n in matches:
        if m.distance < 0.7*n.distance:
            good.append(m)

    numberOfGoodMatches = len(good)
    print("NUMBER OF GOOD MATCHES: " + str(numberOfGoodMatches)) 

    if (numberOfGoodMatches == 0):
        return 0
    if (numberOfGoodMatches > 100):
        return 100
    return numberOfGoodMatches
    

def createResult():
    return jsonify(
        name="Nordwestfassade",
        parent="Altes Rathaus, Bamberg",
        description="Ursprünglich 1755 von Johann Anwander geschaffen und vielfach restauriert, u.a. 1959-1962 durch Anton Greiner. Beide Gebäudeseiten sind vollständig mit allegorischen Szenen und architektonischen Details verziert.",
        quality=calculateQuality()
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