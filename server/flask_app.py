import cv2
from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

URI = "mysql://{username}:{password}@{hostname}/{databasename}".format(username='cwittmann',
password='cW53a8x6',
hostname='cwittmann.mysql.pythonanywhere-services.com',
databasename='cwittmann$default')
app.config['SQLALCHEMY_DATABASE_URI']= URI
app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Building(db.Model):

  __tablename__='building'

  id=db.Column(db.Integer, primary_key=True)
  name=db.Column(db.Text)
  description=db.Column(db.Text)
  lat=db.Column(db.Text)
  lng=db.Column(db.Text)
  parentId=db.Column(db.Integer)
  imageData=db.Column(db.LargeBinary)
  descriptor=db.Column(db.LargeBinary)

db.create_all()
db.session.commit()

def getBestMatch(userLat, userLng):

    userLatFloat = float(userLat)
    userLngFloat = float(userLng)

    # upperLatBound = userLatFloat + 0.001
    # lowerLatBound = userLatFloat - 0.001
    # leftLngBound = userLngFloat - 0.001
    # rightLngBound = userLngFloat + 0.001

    upperLatBound = userLatFloat + 1
    lowerLatBound = userLatFloat - 1
    leftLngBound = userLngFloat - 1
    rightLngBound = userLngFloat + 1

    allBuildings = Building.query.all()
    buildingsInRange = []

    for building in allBuildings:
        if float(building.lat) < upperLatBound and float(building.lat) > lowerLatBound and float(building.lng) > leftLngBound and float(building.lng) < rightLngBound:
            buildingsInRange.append(building)

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


def createResult(userLat, userLng):

    bestMatchId, bestMatchCertainty = getBestMatch(userLat, userLng)
    matchedBuilding = Building.query.get(bestMatchId)

    print(str(matchedBuilding.name))

    return jsonify(
        id=matchedBuilding.id,
        name=matchedBuilding.name,
        description=matchedBuilding.description,
        certainty=bestMatchCertainty
    )

@app.route('/', methods = ['GET', 'POST'])
def returnResult():
    if request.method == 'POST':

        if request.form["userLat"] and request.form["userLng"]:
            userLat = request.form["userLat"]
            userLng = request.form["userLng"]
            print("USER COORDS: ")
            print(str(userLat))
            print(str(userLng))

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
            return createResult(userLat, userLng)

@app.route('/insert', methods=['GET', 'POST'])
def insert():

    id = request.form["id"]
    name = request.form["name"]
    description = request.form["description"]
    lat = request.form["lat"]
    lng = request.form["lng"]
    parentId = request.form["parentId"]

    insert_this = Building(id=id, name=name, description=description, lat=lat, lng=lng, parentId=parentId, imageData=None, descriptor=None)

    db.session.add(insert_this)
    db.session.commit()

    if request.files == None:
            print("NO FILES")

    file = request.files['photo']

    if file is None:
        print('=== NO FILE NAMED FILE ===')

    if file.filename == '':
        print('=== NO SELECTED FILE ===')

    if file:
        print('=== FILE FOUND ===')
        file.save('./uploads/' + str(id) + '.jpeg')
        print('=== FILE SAVED ===')

    return 'Successfully inserted record.'

@app.route('/deleteAll')
def deleteAll():
    db.session.query(Building).delete()
    db.session.commit()
    return 'Successfully deleted all records.'

@app.route('/delete/<buildingId>', methods=['GET', 'POST'])
def delete(buildingId):
    Building.query.filter_by(id=buildingId).delete()
    db.session.commit()
    return 'Successfully deleted record.'

@app.route('/buildings')
def buildings():
    results = Building.query.all()
    return render_template('buildings.html', results = results)

@app.route('/image/<imageId>')
def image(imageId):
    fileName = '/home/cwittmann/uploads/' + str(imageId) + '.jpeg'
    return send_file(fileName, mimetype='image/jpeg')

# app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

# curl -F "file=@image.jpg" http://localhost:8000/home