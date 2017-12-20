from app import db
import Bus

#Bus  table
class Bus(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	busName = db.Column(db.String(80))
	busStatus = db.Column(db.String(80))
	
	def __init__(self, busName, busStatus):
		self.busName=busName
		self.busStatus=busStatus

class Info(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(80))
	
	def __init__(self, password):
		self.password=password
		
def getAllBuses():
	buses=[]
	rs=Bus.query.all()
	for i in rs:
		bus=Bus(i.busName, i.busStatus)
		buses.append(bus)
	return buses
	