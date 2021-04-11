from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False)
    verified_email = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    picture = db.Column(db.String(100), nullable = False)
    locale = db.Column(db.String(50), nullable = False)

    def __init__(self,email,verified_email,name,picture,locale):
        self.email = email
        self.verified_email = verified_email
        self.name = name 
        self.picture = picture
        self.locale = locale

    def __repr__(self):
        return f"{self.name},{self.verified_email},{self.name}, {self.picture}, {self.locale}"
    
    

