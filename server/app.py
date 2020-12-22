from flask import Flask, render_template, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, login_required, LoginManager, logout_user
from sqlalchemy import Column, String, Integer
from flask_wtf import FlaskForm
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
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)


class User(UserMixin, db.Model):
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
    if current_user.is_authenticated:
        auth = True
    else:
        auth = False
    return render_template('index.html', auth=auth)


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            flash('User ' + username + ' already exists')
        else:
            db_add_user(username, password)
            user_object = User.query.filter_by(username=username).first()
            user_object.authenticated = True
            login_user(user_object)
            return redirect(url_for('profile_page', username=username))

    return render_template('formregister.html', title='Registration', form=form)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None or user_id != 'None':
        return User.query.get(user_id)
    else:
        return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile_page'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user_object = User.query.filter_by(username=username, password=password).first()
        if user_object:
            user_object.authenticated = True
            login_user(user_object)
            return redirect(url_for('profile_page', username=username))
        else:
            flash('Invalid username or password')

    return render_template('formlogin.html', title='Sign In', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index_page'))


@app.route('/profile',  methods=['GET'])
@login_required
def profile_page():
    # TODO: profilization, add html
    return render_template('profile.html', username=current_user.username)


@app.route('/portfolio', methods=['GET'])
@login_required
def portfolio_page():
    # TODO: add html
    return 'Portfolio Page'


def db_add_user(username, password):
    db.session.add(User(username, password))
    db.session.commit()


if __name__ == '__main__':
    # db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
