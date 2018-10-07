import time
import cv2
import base64
import numpy as np
import copy
from frame import Frame
from flask import Flask, request, abort, send_file


app = Flask(__name__)


buffer = []


@app.route('/upload', methods=['POST'])
def upload():
    """Upload image to server."""
    if request.method == 'POST':
        buf = base64.b64decode(request.data)
        img = np.frombuffer(buf, dtype='uint8')
        if len(buffer) >= 10:
            buffer.pop()
        buffer.append(Frame(cv2.imdecode(img, 1)))
        buffer[-1].process()
        return "Done"
    else:
        return abort(406)


@app.route('/results', methods=['GET'])
def results():
    if len(buffer) == 0:
        return "0,0,0"
    frame = buffer[-1]
    if not frame.processed:
        frame = buffer[-2]
    print("[Info] Excentration", frame.extentration)
    print("[Info] Distance", frame.distance)
    return frame.giveDirection()


@app.route('/debug', methods=['GET'])
def debug():
    if len(buffer) == 0:
        return "No frames in buffer"
    else:
        image = buffer[-1]
        if image.processed:
            img = copy.deepcopy(image.image)
            if image.rect is not None:
                xa, ya, xb, yb = image.rect
                cv2.rectangle(img, (xa, ya), (xb, yb), (0, 255, 0), 2)
                cv2.putText(img, "Distance to object (m): "+str(image.distance), (10,10), cv2.FONT_HERSHEY_PLAIN, 1, 255)
            cv2.imwrite('/tmp/img.jpg', img)
            return send_file('/tmp/img.jpg')
        else:
            return "No processed yet"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
