import cv2
import base64
import numpy as np
from frame import Frame
from flask import Flask, request, abort


app = Flask(__name__)


dataframe = []

@app.route('/upload', methods=['POST'])
def upload():
    """Upload image to server."""
    if request.method == 'POST':
        buf = base64.b64decode(request.data)
        img = np.frombuffer(buf, dtype='uint8')
        dataframe.append(Frame(cv2.imdecode(img, 1)))
        return "Done"
    else:
        return abort(406)

@app.route('/results', methods=['GET'])
def results():
    return "255;255;0"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
