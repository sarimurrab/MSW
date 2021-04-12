from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from authlib.integrations.flask_client import OAuth
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user



app = Flask(__name__)
base = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+ os.path.join(base, "users.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)

oauth = OAuth(app)

app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
app.config['GOOGLE_CLIENT_ID'] = "1001855844799-rm6ju60atrloq6vb4bm62ud35v743f8o.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "b8pXtFpO1-MlyT0B7MKfQcvZ"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Users(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(100), nullable = False)
    verified_email = db.Column(db.String(100), nullable = False)
    name = db.Column(db.String(100), nullable = False)
    picture = db.Column(db.String(100), nullable = False)
    locale = db.Column(db.String(50), nullable = False)
    coach = db.relationship('Coach', backref='users', lazy=True)

    def __init__(self,email,verified_email,name,picture,locale):
        self.email = email
        self.verified_email = verified_email
        self.name = name 
        self.picture = picture
        self.locale = locale

    def __repr__(self):
        return f"{self.email},{self.verified_email},{self.name}, {self.picture}, {self.locale}"

class Coach(db.Model, UserMixin):
    __tablename__ = "coach"
    id = db.Column(db.Integer, primary_key = True)
    position = db.Column(db.String(100), nullable = False)
    organization = db.Column(db.String(100), nullable = False)
    country = db.Column(db.String(100), nullable = False)
    linkedin = db.Column(db.String(100), nullable = False)
    twitter = db.Column(db.String(50), nullable = False)
    shortdescription = db.Column(db.String(50), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)


    def __init__(self,position,organization,country,linkedin,twitter,shortdescription):
        self.position = position
        self.organization = organization
        self.country = country 
        self.linkedin = linkedin
        self.twitter = twitter
        self.shortdescription = shortdescription
        self.user_id = Users.query.filter_by(email='arsalan1406@gmail.com').first().id

    def __repr__(self):
        return f"{self.position},{self.organization},{self.country}, {self.linkedin}, {self.twitter}, {self.shortdescription}"


google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
)





# Default route
@app.route('/')
def index():
  return render_template('index2.html')


# Google login route
@app.route('/login/google')
def google_login():
   google = oauth.create_client('google')
   redirect_uri = url_for('google_authorize', _external=True)
   return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
   google = oauth.create_client('google')
   token = google.authorize_access_token()
   resp = google.get('userinfo').json()
   if Users.query.filter_by(email=resp['email']).first():
      pass
   else:
      g_user = Users(resp['email'], resp['verified_email'], resp['name'], resp['picture'], resp['locale'])
      db.session.add(g_user)
      db.session.commit()
   user = Users.query.filter_by(email=resp['email']).first()
   login_user(user)
   return f"{Users.query.all()}"




@app.route('/becomecoach', methods = ['POST','GET'])
def becomecoach():
   if request.method == 'POST':
      if not request.form['position'] or not request.form['organization'] or not request.form['country'] or not request.form['linkedin'] or not request.form['shortdescription']:
         flash('Please enter all the fields', 'error')
      else:
         coach = Coach(request.form['position'],request.form['organization'], request.form['country'],
            request.form['linkedin'], request.form['twitter'], request.form['shortdescription'])
         
         db.session.add(coach)
         db.session.commit()
         flash('Record was successfully added')
         return "redirect(url_for('show_all'))"
   return render_template('become_a_coach.html')

@app.route('/logout')
@login_required
def logout():
   logout_user()
   flash("You logged out!")
   return redirect(url_for('index'))

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)

