from enum import unique
from flask import Flask, json, render_template, url_for, redirect, flash, request, jsonify, session
from authlib.integrations.flask_client import OAuth
from flask.templating import render_template_string
from flask_login.utils import login_fresh
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_login import LoginManager, login_required, login_user, UserMixin, logout_user, current_user
from flask_socketio import SocketIO, _ManagedSession, send, emit, join_room, leave_room
import time
from utils.fetch import search
import random
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy_json import mutable_json_type
from utils.entity_recog import entity_recognition



app = Flask(__name__)
base = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:mypassword@localhost/startup1"

#"postgres://djlxcnduwrwmfa:425706efc7122753c64944086c16d981e9230a1687edd9dbf3899950a4371a04@ec2-23-23-164-251.compute-1.amazonaws.com:5432/d91fikrbh1bka4"
# "sqlite:///" + \
#     os.path.join(base, "users.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

socketio = SocketIO(app,manage_session=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


oauth = OAuth(app)

app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
app.config['GOOGLE_CLIENT_ID'] = "1001855844799-rm6ju60atrloq6vb4bm62ud35v743f8o.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "b8pXtFpO1-MlyT0B7MKfQcvZ"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


##########################################
############### UTILS ####################
##########################################




class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    verified_email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    picture = db.Column(db.String(100), nullable=False)
    locale = db.Column(db.String(50), nullable=False)
    coach = db.relationship('Coach', backref='users', lazy=True)

    def __init__(self, username, email, verified_email, name, picture, locale):
        self.username = username.split('@')[0]
        self.email = email
        self.verified_email = verified_email
        self.name = name
        self.picture = picture
        self.locale = locale

    def __repr__(self):
        return f"{self.id},{self.username},{self.email},{self.verified_email},{self.name}, {self.picture}, {self.locale}"



class Coach(db.Model, UserMixin):
    __tablename__ = "coach"
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.String(100), nullable=False)
    organization = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)
    linkedin = db.Column(db.String(100), nullable=False)
    twitter = db.Column(db.String(50), nullable=False)
    github = db.Column(db.String(50), nullable=False)
    skypeid = db.Column(db.String(50), nullable=False)
    shortdescription = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, position, organization, country, linkedin, twitter, github, skypeid,shortdescription):
        self.position = position
        self.organization = organization
        self.country = country
        self.linkedin = linkedin
        self.twitter = twitter
        self.github = github
        self.skypeid = skypeid
        self.shortdescription = shortdescription
        self.user_id = User.query.filter_by(
            email=session['current_email']).first().id

    def __repr__(self):
        return f"{self.id},{self.position},{self.organization},{self.country}, {self.linkedin}, {self.twitter},{self.github},{self.skypeid}, {self.shortdescription}"


class Requests(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    requests = db.Column(mutable_json_type(dbtype=JSONB, nested=True))
    mentors_accepted_me = db.Column(mutable_json_type(dbtype=JSONB, nested=True))

    def __init__(self, requests,mentors_accepted_me):
        self.requests = requests
        self.mentors_accepted_me = mentors_accepted_me
    def __repr__(self):
        return f"{self.id},{self.requests},{self.mentors_accepted_me}"

google = oauth.register(
    name='google',
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    # This is only needed if using openId to fetch user info
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)


# Default route
@app.route('/')
def index():
    # tmp_mail = None
    # try:
    #   tmp_mail = session['current_email']
    # except:
    #   pass
    allowed_to_coach = None
    # if tmp_mail != None:
    #    id_ = User.query.filter_by(email=tmp_mail).first().id
    #    if len(Coach.query.filter_by(id=id_).all()) >= 1:
    #       allowed_to_coach = False
    #    else:
    #       allowed_to_coach = True
    try:
        coach = Coach.query.filter_by(id=current_user.id).first()
        print(coach)
    except:
        coach = None
    if coach:
        allowed_to_coach = False
    else:
        allowed_to_coach = True



    num_of_notifications = 0
    if current_user.is_active:
        mentor_username,mentor_id = current_user.username, current_user.id
        list_of_requests = Requests.query.filter_by(id=mentor_id).first().requests[mentor_username]
        for i in list_of_requests:
            if list_of_requests[i]=='req_came':
                num_of_notifications+=1
            
    
    
    return render_template('index2.html',allowed_to_coach=allowed_to_coach,num_of_notifications=num_of_notifications)


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
    if User.query.filter_by(email=resp['email']).first():
        pass
    else:
        print('Here')
        g_user = User(resp['email'],resp['email'], resp['verified_email'],
                       resp['name'], resp['picture'], resp['locale'])
        
        db.session.add(g_user)
        db.session.commit()

        #Intialize with Zero value
        start_json = {resp['email'].split('@')[0]: {}} 
        start_json_list = {resp['email'].split('@')[0]: []} 
        requests_per_user = Requests(requests=start_json,mentors_accepted_me=start_json_list)
        db.session.add(requests_per_user)
        db.session.commit()

        
        
    session['current_email'] = resp['email']
    user = User.query.filter_by(email=resp['email']).first()
    
    login_user(user)
    
    return redirect(url_for('index'))


@app.route('/becomecoach', methods=['POST', 'GET'])
@login_required
def becomecoach():
    if request.method == 'POST':
        if not request.form['position'] or not request.form['organization'] or not request.form['country'] or not request.form['linkedin'] or not request.form['shortdescription']:
            flash('Please enter all the fields', 'error')
        else:
            coach = Coach(request.form['position'], request.form['organization'], request.form['country'],
                          request.form['linkedin'], request.form['twitter'],request.form['github'],request.form['skypeid'], request.form['shortdescription'])

            db.session.add(coach)
            db.session.commit()
            flash('Record was successfully added')
            return redirect(url_for('list_of_coach'))
    return render_template('become_a_coach.html')


@app.route('/list-of-coach')
@login_required
def list_of_coach():
    result = db.session.query(User, Coach).join(Coach).all()
    mentor_alwd_mente_lst = Requests.query.get(current_user.id).mentors_accepted_me[current_user.username]

    return render_template('list_of_coach.html', result=result,mentor_alwd_mente_lst=mentor_alwd_mente_lst)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You logged out!")
    return redirect(url_for('index'))


@app.route('/profile')
@login_required
def profile():
    coach_object = Coach.query.filter_by(id = current_user.id).first()
    
    return render_template('profile_user.html',coach_object = coach_object)

# User(resp['email'],
# resp['email'], resp['verified_email'],
#                        resp['name'], resp['picture'], resp['locale'])

@app.route('/profile_edit',methods = ['POST','GET'])
@login_required
def profile_edit():
    coach_object = Coach.query.filter_by(id = current_user.id).first()
    if request.method == 'POST':
        current_user.name = request.form['name']
        coach_object.position , coach_object.organization= request.form['position'], request.form['organization']

        coach_object.country , coach_object.linkedin= request.form['country'], request.form['linkedin']

        coach_object.github , coach_object.twitter= request.form['github'], request.form['twitter']

        coach_object.skypeid , coach_object.shortdescription= request.form['skypeid'], request.form['shortdescription']

        db.session.commit()
        return redirect(url_for('profile'))
    
    return render_template('profile_user_edit.html',coach_object = coach_object)

@app.route('/services')
@login_required
def services():
    return render_template('services.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/proposal', methods=['POST','GET'])
def proposal():
    if request.method == 'POST':
        ques1 = entity_recognition(request.form['otherDetails'])+" "+"startup goverment schemes"
        list_of_ques = [ques1]

        all_recommendations = []
        for ques in list_of_ques:
            for i in search(ques,num_results=30):
                all_recommendations.append(i)  
        return render_template('sys_recommendation_after.html',all_recommendations=all_recommendations)
    return render_template('NLP.html')

@app.route('/system-recommendation', methods=['POST','GET'])
@login_required
def system_recommend():
    if request.method == 'POST':
        session["category"] = request.form['Category']
        session["industry"] = request.form['IndustryCategory']
        session['topic'] = request.form['topic']
        session["type"] = request.form['type']
        session["budget"] = request.form['budget']
        session["mode"] = request.form['mode']
        session["location"] = request.form['location']
        session["funding"] = request.form['funding']
        session["otherDetails"] = request.form['otherDetails']
        return redirect(url_for('system_recommend_after'))

    return render_template('sys_recommendation.html')

@app.route('/system-recommendation-result')
@login_required
def system_recommend_after():
    list_of_bgs = ["card text-white bg-primary mb-3","card text-white bg-secondary mb-3","card text-white bg-success mb-3","card text-white bg-danger mb-3","card text-white bg-warning mb-3","card text-white bg-info mb-3","card bg-light mb-3","card text-white bg-dark mb-3"]
    ques1 = "Who can help for startup in "+session['industry']
    ques2 = "List of Government Schemes To Support " +session["industry"]+" "+"Startups In "+session["location"]
    ques3 = session['type']+" private startup schemes related to "+session['industry']
    ques4 = "Venture funding for "+session['industry']+" startups in "+session['location']+" upto "+session['funding']
    ques5 = "Seed funding for "+session['industry']+" startups in "+session['location']+" upto "+session['funding']
    ques6 = "Platforms that provide funding for "+session['industry']+" startups in "+session['location']+" upto "+session['funding']
    ques7 = "Startup "+session['otherDetails']+" Details help"
    ques8 = "Which organisations provide "+session['funding']+" for "+session['industry']+" related startup"
    ques9 = "Innovative ideas for "+session['topic']+" startup."

    list_of_ques = [ques2,ques1,ques3,ques4,ques5,ques6,ques7,ques8,ques9]
    num_results_choices = [4,5,6,7,8,9]
    
    all_recommendations = []
    for ques in list_of_ques:
        num_results = random.choice(num_results_choices)
        for i in search(ques,num_results=num_results):
            all_recommendations.append(i)

    
    return render_template('sys_recommendation_after.html',all_recommendations=all_recommendations)


@app.route('/send-request/<rcvd_username>')
@login_required
def send_request(rcvd_username):
    mentee_username = current_user.username
    mentor_username = rcvd_username
    mentor_id = User.query.filter_by(username = mentor_username).first().id
    obj_mentor_requests = Requests.query.filter_by(id = mentor_id).first()

    mentor_python_dict = dict(obj_mentor_requests.requests)
    print(obj_mentor_requests)
    mentor_python_dict[mentor_username][mentee_username] = "req_came"
    # print(mentor_python_dict)
    # print(obj_mentor_requests.requests[mentor_username])
    obj_mentor_requests.requests =mentor_python_dict
    # print(obj_mentor_requests.requests[mentor_username])
    print(obj_mentor_requests)
    db.session.add(obj_mentor_requests)
    db.session.commit()
    print(Requests.query.filter_by(id = mentor_id).first())
    # obj_mentor_requests.requests =  mentor_python_dict
    # db.session.commit()
    print(Requests.query.all())
    return {"SENDER": current_user.username, "TO":rcvd_username}


@app.route('/notifications')
@login_required
def notifications():
    mentor_username,mentor_id = current_user.username, current_user.id
    list_of_requests = Requests.query.filter_by(id=mentor_id).first().requests[mentor_username]

    num_of_notifications = 0
    if current_user.is_active:
        mentor_username,mentor_id = current_user.username, current_user.id
        list_of_requests = Requests.query.filter_by(id=mentor_id).first().requests[mentor_username]
        for i in list_of_requests:
            if list_of_requests[i]=='req_came':
                num_of_notifications+=1
    
    return render_template('req_notifications.html', list_of_requests = list_of_requests, num_of_notifications=num_of_notifications)

@app.route('/reqserve_accept/<mentees_username>')
@login_required
def reqserve_accept(mentees_username):
    mentees_id = User.query.filter_by(username = mentees_username).first().id
    obj_for_mentees = Requests.query.get(mentees_id)
    mentees_python_dict = dict(obj_for_mentees.mentors_accepted_me)
    mentees_python_dict[mentees_username].append(current_user.username)

    obj_for_mentees.mentors_accepted_me = mentees_python_dict
    db.session.add(obj_for_mentees)
    db.session.commit()

    mentors_object = Requests.query.get(current_user.id)
    mentors_python_dict = dict(mentors_object.requests)
    mentors_python_dict[current_user.username][mentees_username] = 'req_accepted'
    mentors_object.requests = mentors_python_dict
    db.session.add(mentors_object)
    db.session.commit()


    return redirect(url_for('index'))


@app.route('/reqserve_reject/<mentees_username>')
@login_required
def reqserve_reject(mentees_username):
    mentors_object = Requests.query.get(current_user.id)
    mentors_python_dict = dict(mentors_object.requests)
    mentors_python_dict[current_user.username][mentees_username] = 'req_rejected'
    mentors_object.requests = mentors_python_dict
    db.session.add(mentors_object)
    db.session.commit()


    return redirect(url_for('index'))
    


ROOMS = ["Education", "news", "games", "coding"]
@app.route('/chat')
def chat():

    if not current_user.is_authenticated:
        flash('Please login', 'danger')
        return redirect(url_for('login'))

    return render_template("chat.html", username=current_user.username, rooms=ROOMS)

@socketio.on('incoming-msg')
def on_message(data):
    """Broadcast messages"""

    msg = data["msg"]
    username = data["username"]
    room = data["room"]
    # Set timestamp
    time_stamp = time.strftime('%b-%d %I:%M%p', time.localtime())
    send({"username": username, "msg": msg, "time_stamp": time_stamp}, room=room)


@socketio.on('join')
def on_join(data):
    """User joins a room"""

    username = data["username"]
    room = data["room"]
    join_room(room)

    # Broadcast that new user has joined
    send({"msg": username + " has joined the " + room + " room."}, room=room)


@socketio.on('leave')
def on_leave(data):
    """User leaves a room"""

    username = data['username']
    room = data['room']
    leave_room(room)
    send({"msg": username + " has left the room"}, room=room)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
