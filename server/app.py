from flask import Flask, request, Response, json, jsonify, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',  # Default is '{{', I'm changing this because Vue.js uses '{{' / '}}'
        variable_end_string='%%',
    ))


app = CustomFlask(__name__)
app.config['SECRET_KEY'] = 'secretkey'


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit Form')


@app.route('/')
def index_page():
    # rates will be here
    # TODO: fix attaching the index.js file to index.html
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration_page():
    form = LoginForm()
    return render_template('formregister.html', title='Registration', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('formlogin.html', title='Sign In', form=form)


@app.route('/profile',  methods=['GET'])
def profile_page():
    return 'Profile Page'


@app.route('/portfolio', methods=['GET'])
def portfolio_page():
    return 'Portfolio Page'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
