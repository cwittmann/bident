from flask import Flask, jsonify, redirect, request, Response
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename

app = Flask(__name__)
cors = CORS(app)

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
            return "FILE UPLOADED SUCCESSFULLY"

app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

# curl -F "file=@image.jpg" http://localhost:8000/home