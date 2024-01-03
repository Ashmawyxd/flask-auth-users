from flask import Flask, render_template, request, redirect, url_for, session , flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from models.models import db
from views.auth import auth as auth_blueprint
from views.home import home as home_blueprint

app = Flask(__name__)
app.secret_key = "hello"

# Initialize database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['UPLOAD_FOLDER'] = 'uploads/users_image'  # Create this folder in the same directory as your app.py file
app.permanent_session_lifetime = timedelta(days=5)
db.init_app(app)

# Create the database tables
with app.app_context():
    db.create_all()

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(home_blueprint, url_prefix='/home')

#################################################### welcom route ###############################################
@app.route("/")
def home():
    return render_template('home.html', contact="ahmed")

if __name__ == "__main__":
    app.run(debug=True)
