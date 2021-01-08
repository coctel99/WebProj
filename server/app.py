from flask import Flask, render_template, flash, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, current_user, login_user, login_required, LoginManager, logout_user
from sqlalchemy import Column, String, Integer, update
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
    cryptolist = Column(String(2048))

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cryptolist = ""

    def __repr__(self):
        return "{}".format(self.username)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit Form')


class OverlayForm(FlaskForm):
    input = StringField('Input', validators=[DataRequired()])
    value = StringField('Value')
    submit = SubmitField('Submit Form')


@app.route('/', methods=['GET', 'POST'])
def index_page():
    if current_user.is_authenticated:
        auth = True
    else:
        auth = False

    form = OverlayForm()
    if form.validate_on_submit():
        input = form.input.data
        value = form.value.data
        curr, val = unpack(current_user.cryptolist)
        index1 = curr.index('ETH')
        index2 = curr.index('BTC')
        val1 = val[index1]
        val2 = val[index2]

    return render_template('index.html', auth=auth, form=form)


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
    return redirect(url_for('login'))


@app.route('/profile',  methods=['GET'])
@login_required
def profile_page():
    cur_usr = current_user
    # TODO: add html and css
    return render_template('profile.html', username=current_user.username)


@app.route('/portfolio', methods=['GET'])
@login_required
def portfolio_page():
    cur_usr = current_user
    curr, val = parse_list(current_user.cryptolist)
    # TODO: add html and css, show user's cryptocurrancy
    return render_template('portfolio.html', username=current_user.username, curr=curr, val=val)


def db_add_user(username, password):
    db.session.add(User(username, password))
    db.session.commit()


def parse_list(cryptolist):
    curr = []
    val = []
    cryptolist = cryptolist[:-1]
    list = cryptolist.split(';')
    for i in range(len(list)):
        currval = list[i]
        currval = list[i].split(':')
        curr.append(currval[0])
        val.append(currval[1])

    curr = '\n'.join(curr)
    val = '\n'.join(val)
    return curr, val


def unpack(cryptolist):
    curr = []
    val = []
    cryptolist = cryptolist[:-1]
    list = cryptolist.split(';')
    for i in range(len(list)):
        currval = list[i]
        currval = list[i].split(':')
        curr.append(currval[0])
        val.append(currval[1])

    return curr, val


def pack(curr, val):
    list = []
    for i in range(len(curr)):
        currval = curr[i] + ':' + val[i]
        list.append(currval)

    cryptolist = ';'.join(list)
    return cryptolist

if __name__ == '__main__':
    # db.create_all()
    app.run(host='127.0.0.1', port=5000, debug=True)
