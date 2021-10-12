from App import app

from App.api import userController, applicationController, recordController, noticeController, checkinController, hrController
from App.api import userApplicationController, faceDataController



@app.route('/')
def hello_world():
    return 'Hello World!'
