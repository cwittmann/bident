from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import fileHandler
import imageMatcher
import os

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Connect to database
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
  lat=db.Column(db.DECIMAL(9,6))
  lng=db.Column(db.DECIMAL(9,6))
  parentId=db.Column(db.Integer)

db.create_all()
db.session.commit()

# Create result of matching as JSON object
def createResult(allBuildings, userLat, userLng):

    bestMatchId, matchCertainty = imageMatcher.getBestMatch(allBuildings, userLat, userLng)
    matchedBuilding = Building.query.get(bestMatchId)

    if matchedBuilding == None or matchCertainty == None:
        return jsonify(
        success=False
    )

    matchParentId = None
    matchParentName = None

    if matchedBuilding.parentId != None:
        parentBuilding = Building.query.get(matchedBuilding.parentId)

        if parentBuilding != None:
            matchParentId=parentBuilding.id,
            matchParentName=parentBuilding.name

    return jsonify(
        success=True,
        id=matchedBuilding.id,
        name=matchedBuilding.name,
        description=matchedBuilding.description,
        certainty=matchCertainty,
        parentId=matchParentId,
        parentName=matchParentName
    )

@app.route('/', methods = ['POST'])
def returnResult():
    
    if request.form["userLat"] and request.form["userLng"]:
        userLat = request.form["userLat"]
        userLng = request.form["userLng"]

    files = request.files
    filePath = './uploads/blob.jpeg'
    fileHandler.saveFile(files, filePath)

    allBuildings = Building.query.all()

    return createResult(allBuildings, userLat, userLng)

# Insert new building into database and save its image on server
@app.route('/insert', methods=['POST'])
def insert():

    id = request.form["id"]
    name = request.form["name"]
    description = request.form["description"]
    lat = request.form["lat"]
    lng = request.form["lng"]
    parentId = request.form["parentId"]

    insert_this = Building(id=id, name=name, description=description, lat=lat, lng=lng, parentId=parentId)

    db.session.add(insert_this)
    db.session.commit()

    files = request.files
    filePath = './uploads/' + str(id) + '.jpeg'

    return fileHandler.saveFile(files, filePath)

# Delete specified building from database
@app.route('/delete/<buildingId>', methods=['GET', 'POST'])
def delete(buildingId):
    Building.query.filter_by(id=buildingId).delete()
    db.session.commit()

    fileName = '/home/cwittmann/uploads/' + str(buildingId) + '.jpeg'
    os.remove(fileName)
    return 'Successfully deleted record.'

# Get information on specified building
@app.route('/building/<buildingId>')
def building(buildingId):
    result = Building.query.get(buildingId)
    return jsonify(
        success=True,
        id=result.id,
        name=result.name,
        description=result.description
    )

# Show all buildings
@app.route('/buildings')
def buildings():
    results = Building.query.all()   
    return render_template('buildings.html', results = results)

# Get image of building with specified id
@app.route('/image/<imageId>')
def image(imageId):
    fileName = '/home/cwittmann/uploads/' + str(imageId) + '.jpeg'
    return send_file(fileName, mimetype='image/jpeg')

# app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)