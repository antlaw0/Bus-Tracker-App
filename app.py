
import os
from flask import Flask, render_template, request, redirect
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

		
@app.route('/')
def home_page():
	buses=models.getAllBuses()
	
	return render_template("index.html", buses=buses)


@socketio.on('new_message')
def handle_new_message(message):
    print("New message recieved: ", message)
	
    # Broadcast the messsage to all connected clients.
    emit("new_message_received", message, broadcast=True)

@app.route('/admin', methods=['POST','GET'])
def admin():
	if request.method=='POST':
		if 'newBus' in request.form:
			b=models.Bus(request.form['newBus'], 'unarrived')
			db.session.add(b)
			db.session.commit()
			
		if 'busToDelete' in request.form:
			print("Bus to delete: "+request.form['busToDelete'])
			b=models.Bus.query.filter_by(busName=request.form['busToDelete']).first()
			db.session.delete(b)
			db.session.commit()
	buses=models.getAllBuses()		
	return render_template('admin.html', buses=buses)
	
@app.route('/updateDatabase', methods=['POST'])
def updateDatabase():
	busString=request.form['busString']
	busString = busString.split(";")
	busName = busString[0]
	busStatus = busString[1]
	b=models.Bus.query.filter_by(busName=busName).first()
	b.busStatus=busStatus
	db.session.add(b)
	db.session.commit()
	buses=models.getAllBuses()
	return render_template('index.html', buses=buses)

if __name__ == '__main__':
    socketio.run(app, host="https://agile-sea-57808.herokuapp.com")