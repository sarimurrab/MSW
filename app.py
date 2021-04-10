from flask import Flask, render_template, url_for, redirect
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

oauth = OAuth(app)

app.config['SECRET_KEY'] = "THIS SHOULD BE SECRET"
app.config['GOOGLE_CLIENT_ID'] = "1001855844799-rm6ju60atrloq6vb4bm62ud35v743f8o.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "b8pXtFpO1-MlyT0B7MKfQcvZ"


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
  return render_template('index.html')


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
    print(f"\n{resp}\n")
    return "You are successfully signed in using google"




if __name__ == '__main__':
  app.run(debug=True)