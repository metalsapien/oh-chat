''' This module is responsible for starting the app/server '''
from ohchat import app, socketio


if __name__ == '__main__':
    socketio.run(app,
                 host='0.0.0.0',
                 port=5000)
