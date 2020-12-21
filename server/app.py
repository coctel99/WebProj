import flask
from flask import Flask, request, Response, json, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Column, String, Integer
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' and '}} too'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/crypto.db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True)
    password = Column(String(24))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "{}".format(self.username)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit Form')


@app.route('/')
def index_page():
    # rates will be here
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # TODO: check if exists

        db_add_user(username, password)
        return flask.redirect('/profile')

    return render_template('formregister.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return flask.redirect('/profile')
    return render_template('formlogin.html', title='Sign In', form=form)


@app.route('/profile',  methods=['GET'])
def profile_page():
    # TODO: profilization, add html
    return 'Profile Page'


@app.route('/portfolio', methods=['GET'])
def portfolio_page():
    # TODO: add html
    return 'Portfolio Page'


def db_add_user(username, password):
    db.session.add(User(username, password))
    db.session.commit()
    print("DB: Created user ", username, password)


if __name__ == '__main__':
    #db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
