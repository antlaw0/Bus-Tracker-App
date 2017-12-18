from app import db

#User accounts table
class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80))
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(80))
	status = db.Column(db.String(200)) #stores info about state of game
	character1 = db.Column(db.String(10000))
	character2 = db.Column(db.String(10000))
    
	def __init__(self, email, username,password):
		self.username = username
		self.email = email
		self.password=password
		self.status=""
		#init status string
		for i in range(100):
			self.status+="0;"