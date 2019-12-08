from flask import Flask
app = Flask(__name__)

@app.route("/home/pi", methods = ['POST'])
def pi():
    data = request.form['data']

if __name__ == "__main__":
    app.run()