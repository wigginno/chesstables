from flask import Flask, render_template
from flask import request, redirect
webapp = Flask(__name__)

@webapp.route('/hello')
def hello():
    return "Hello!"

@webapp.route('/')
def index():
    return "<p>hi</p>"

@webapp.route('/home')
def home():
    return render_template('home.html', result = result)
