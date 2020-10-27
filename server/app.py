from flask import Flask, request, Response, json, jsonify
app = Flask(__name__)


@app.route('/')
def index_page():
    # rates will be here
    return 'Index Page'


@app.route('/registration')
def registration_page():
    return 'Registration Page'


@app.route('/login')
def login_page():
    return 'Login Page'


@app.route('/account')
def account_page():
    return 'Account Page'


@app.route('/cryptopackage')
def cryptopackage_page():
    return 'Cryptopackage Page'


if __name__ == '__main__':
    app.run(debug=True, port=5001)
