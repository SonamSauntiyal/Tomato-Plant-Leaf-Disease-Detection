import os
# from . api.main import predict
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import json

UPLOAD_FOLDER = r'./static/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        # check if the post request has the file part
        print(request.files)
        if 'img' not in request.files:
            flash('No file part')
            return "FILE NOT FOUND"
        file = request.files['img']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "FILE NAME NOT FOUND"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            
            import requests
            MODEL_URL = "http://localhost:3001/predict"
            
            files = {'file': open(UPLOAD_FOLDER+filename, 'rb')}
            x = requests.post(MODEL_URL, files=files)
            # x = requests.post(MODEL_URL,data={'file':})
            # print(x.text["class"] + " " + x.text["c"])
            # clf_class = x.text['class']
            # clf_confi = x.text['confidence']
            # print(x.json['class'])
            # print(type(x.text))
            # return str(type(x.content))
            data = x.text
            data=json.loads(data)
            return render_template('predict.html', data=data)
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)