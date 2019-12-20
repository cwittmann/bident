from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'bmp'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
CORS(app)

@app.route('/', methods = ['GET', 'POST'])
def returnResult():
    if request.method == 'POST':
        print('=== UPLOAD ATTEMPTED ===')
        
        if request.files == None:
            print("NO FILES")
        
        print(len(request.files))        

        file = request.files['file']        

        if file is None:
            print('=== NO FILE NAMED FILE ===')
            return "ERROR"
        else:
            print('=== FILE FOUND ===')
            print(file)            
        
        if file.filename == '':
            print('=== NO SELECTED FILE ===')
            return "ERROR"
        if file:
            print('=== FILE FOUND ===')
            filename = secure_filename(file.filename)
            file.save('./uploads/' + str(filename))
            print('=== FILE SUCCESSFULLY UPLOADED ===')
            return "SUCCESS"

# app.run(port=8000, debug=True)

# curl -F "file=@image.jpg" http://localhost:8000/home