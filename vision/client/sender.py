import requests
from capture import imageAsBase64

s = requests.Session()
server_ip = "192.169.0.231"
port = 8000
path = "/upload"
url = "http://" + server_ip + ":" + str(port) + path

def send():
    """Send capture to server."""
    s.post(url, data=imageAsBase64())
