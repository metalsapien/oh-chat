''' Package to initialize the app '''

from flask import Flask
from flask_socketio import SocketIO


# Initializing the app
app = Flask(__name__)
app.config.from_object('settings')
# Initiliazing flask-socketio
socketio = SocketIO(app)

# Importing routes/functions used by the app
from user import views
