from flask import Flask, render_template, request, redirect, url_for, session , flash ,Blueprint
home = Blueprint('home', __name__, static_folder='static', template_folder='templates')
from models.models import User,admins,db

############################################### home route #######################################################
@home.route("/")
def index():
    return render_template('home.html', contact="ahmed")
