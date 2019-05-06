import logging
import os

from flask import Flask, request, jsonify
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('OVP')

app = Flask(__name__)
app.config['SECRET KEY'] = os.urandom(24)
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/upload", methods=['POST'])
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
def upload():
    target = UPLOAD_FOLDER
    if not os.path.isdir(target):
        os.mkdir(target)
    image = request.files['file']
    filename = secure_filename(image.filename)
    destination = "/".join([target, filename])
    image.save(destination)
    logger.info('File Saved: ' + filename)
    return jsonify(success=True)


if __name__ == "__main__":
    app.run()
