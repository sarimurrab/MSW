from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MYKEY'

class Signup_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    confirm_password = StringField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('SIGN UP')


@app.route("/signup")
def signup():
    signupform = Signup_form()
    return render_template('sign_up_page.html',signupform=signupform)


app.run(debug=True)