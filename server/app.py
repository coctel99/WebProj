from flask import Flask, request, Response, json, jsonify, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


@app.route('/')
def index_page():
    # rates will be here
    # TODO: fix attaching the index.js file to index.html
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    return 'Registration Page'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('Formlogin.html', title='Sign In', form=form)


@app.route('/profile',  methods=['GET'])
def profile_page():
    return 'Profile Page'


@app.route('/portfolio', methods=['GET'])
def portfolio_page():
    return 'Portfolio Page'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
