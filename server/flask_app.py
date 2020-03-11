from flask import Flask, jsonify, request, render_template, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import fileHandler
import imageMatcher

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

def createResult(allBuildings, userLat, userLng):

    bestMatchId, bestMatchCertainty = imageMatcher.getBestMatch(allBuildings, userLat, userLng)
    matchedBuilding = Building.query.get(bestMatchId)

    if matchedBuilding == None:
        return 'No match found.'

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

        files = request.files
        filePath = './uploads/blob.jpeg'
        fileHandler.saveFile(files, filePath)
        
        allBuildings = Building.query.all()
        return createResult(allBuildings, userLat, userLng)        

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

    files = request.files
    filePath = './uploads/' + str(id) + '.jpeg'

    return fileHandler.saveFile(files, filePath)    

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