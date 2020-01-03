from flask import Flask, jsonify, redirect, request, Response
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)

def createResult():
    return jsonify(
        name="Nordwestfassade",
        parent="Altes Rathaus, Bamberg",
        description="Ursprünglich 1755 von Johann Anwander geschaffen und vielfach restauriert, u.a. 1959-1962 durch Anton Greiner. Beide Gebäudeseiten sind vollständig mit allegorischen Szenen und architektonischen Details verziert.",
        quality="99.9"
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