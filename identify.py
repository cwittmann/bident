from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/home', methods=['POST'])
def home():
    data = request.files['file']
    return jsonify({"status":"ok"})

app.run(port=8000)

# curl -F "file=@image.jpg" http://localhost:8000/home