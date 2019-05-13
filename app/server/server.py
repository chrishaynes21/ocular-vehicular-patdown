import logging
import os

import image_processing
from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('OVP')

app = Flask(__name__)
app.config['SECRET KEY'] = os.urandom(24)
app.config['CORS_HEADERS'] = 'Content-Type'

UPLOAD_FOLDER = os.path.basename('uploads')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
cors = CORS(app, resources={r"/*": {"origins": "*"}})


def allowed_file(filename):
    logger.info('.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=['POST'])
@cross_origin()
def upload():
    target = UPLOAD_FOLDER
    if not os.path.isdir(target):
        os.mkdir(target)
    image = request.files['file']
    filename = secure_filename(image.filename)
    file_is_allowed = allowed_file(filename)
    logger.info('File is allowed: ' + str(file_is_allowed))
    if file_is_allowed:
        destination = "/".join([target, filename])
        image.save(destination)
        logger.info('File Saved: ' + filename)
        return jsonify(filename)
    else:
        return BadRequest('File must be .JPG or .JPEG')


@app.route('/classification', methods=['GET'])
@cross_origin()
def get_classification():
    file_name = request.args.get('fileName')
    classification = request.args.get('classification')
    logger.info('Classification: ' + classification + 'File: ' + file_name)
    file_path = os.path.join(UPLOAD_FOLDER, file_name)
    classification = classify_image(file_path, classification)
    return jsonify(classification)


def classify_image(file_path, classification):
    image_as_np = image_processing.image_to_numpy(file_path)
    return '1960'


if __name__ == "__main__":
    app.run()
