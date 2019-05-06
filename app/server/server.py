import os
import logging

from flask import Flask, request
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('OVP')

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/upload", methods=['POST'])
def upload():
    target = UPLOAD_FOLDER
    logger.info(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info('Inside upload')
    image = request.files['file']
    filename = secure_filename(image.filename)
    destination = "/".join([target, filename])
    image.save(destination)
    response = 'We did it'
    return response


if __name__ == "__main__":
    app.run(debug=True)
