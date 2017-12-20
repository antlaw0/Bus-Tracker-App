
import os
from flask import Flask, render_template, request, redirect, session, url_for
from flask_socketio import SocketIO, send, emit
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
import models

#db.drop_all()
#db.create_all()
#i=models.Info("KarnerBlue")
#db.session.add(i)
#db.session.commit()
			
socketio = SocketIO(app)

@app.route('/', methods=['POST','GET'])		
def home_page():
	messages=[]
	if 'access' in session:
		return render_template('main.html', buses=models.getAllBuses())
	if 'password' in request.form:
		i=models.Info.query.filter_by(id=1).first()
		#if submitted password matches password in database
		if request.form['password'] == i.password:
			return render_template('main.html',buses=models.getAllBuses())
		else:
			messages.append("Incorrect password. Please try again.")
	session['access']='true'
	return render_template('index.html', messages=messages)
	
@socketio.on('new_message')
def handle_new_message(message):
    print("New message recieved: ", message)
	
    # Broadcast the messsage to all connected clients.
    emit("new_message_received", message, broadcast=True)

@app.route('/admin', methods=['POST','GET'])
def admin():
	messages=[]
	if 'access' not in session:
		messages.append("Please log in to continue.")
		print("access not in session")
		return render_template('index.html', messages=messages)
	if request.method=='POST':
		
		if 'newPassword' in request.form:
			if len(request.form['newPassword']) != 0:
				i=models.Info.query.filter_by(id=1).first()
				i.password=request.form['newPassword']
				db.session.add(i)
				db.session.commit()
				messages.append("Password changed to "+request.form['newPassword'])
				#return redirect(url_for('admin'))
			
		
		if 'newBus' in request.form:
			if len(request.form['newBus']) != 0:
				b=models.Bus(request.form['newBus'], 'unarrived')
				db.session.add(b)
				db.session.commit()
				messages.append(request.form['newBus']+" added.")
				#return redirect(url_for('admin'))
		if 'busToDelete' in request.form:
			if len(request.form['busToDelete']) != 0:
				print("Bus to delete: "+request.form['busToDelete'])
				b=models.Bus.query.filter_by(busName=request.form['busToDelete']).first()
				db.session.delete(b)
				db.session.commit()
				messages.append(request.form['busToDelete']+" has been deleted.")
				#return redirect(url_for('admin'))
	buses=models.getAllBuses()		
	return render_template('admin.html', buses=buses, messages=messages)
	
@app.route('/updateDatabase', methods=['POST','GET'])
def updateDatabase():
	busString=request.form['busString']
	busString = busString.split(";")
	busName = busString[0]
	busStatus = busString[1]
	print("INFO: "+busName+" "+busStatus)
	b=models.Bus.query.filter_by(busName=busName).first()
	b.busStatus=busStatus
	db.session.add(b)
	db.session.commit()
	buses=models.getAllBuses()
	return render_template('main.html', buses=buses)

if __name__ == '__main__':
    socketio.run(app, host="https://agile-sea-57808.herokuapp.com")