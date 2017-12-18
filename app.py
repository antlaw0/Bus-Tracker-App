import os
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
import models

#db.drop_all()
#db.create_all()

socketio = SocketIO(app)

class Bus(object):
	def __init__(self, name, status):
		self.name=name
		self.status=status
		
@app.route('/')
def home_page():
	bus1=Bus("Alpha", "unarrived")
	bus2=Bus("Bravo", "unarrived")
	buses=[]
	buses.append(bus1)
	buses.append(bus2)
	
	return render_template("index.html", buses=buses)


@socketio.on('new_message')
def handle_new_message(message):
    print("New message recieved: ", message)
	
    # Broadcast the messsage to all connected clients.
    emit("new_message_received", message, broadcast=True)



if __name__ == '__main__':
    socketio.run(app, host="https://agile-sea-57808.herokuapp.com")