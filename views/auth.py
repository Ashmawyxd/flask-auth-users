from flask import Flask, render_template, request, redirect, url_for, session , flash ,Blueprint
auth = Blueprint('auth', __name__, static_folder='static', template_folder='templates')
from models.models import User,admins,db
from werkzeug.utils import secure_filename
import os
############################################### user profile route ###############################################
@auth.route("/user")
def user():
    if "username" in session:
        return render_template('accounts/profile.html', username=session["username"], email=session["email"], password=session["password"])
    else:
        return redirect(url_for("auth.login"))
# this rout to get user data from database and compare it username and password with the data from login form and if it's correct it will redirect to profile page and create session for the user

################################## register route to add new user to database #####################################
@auth.route("/register", methods=["POST", "GET"]) 
def register():
    if request.method == "POST":
        # Assuming the form fields are 'username', 'email', and 'password'
        session.permanent = True
        if request.form["username"] == '':
            flash("Please enter your username to register", "info")
            return redirect(url_for("auth.register"))
        elif request.form["email"] == '':
            flash("Please enter your email", "info")
            return redirect(url_for("auth.register"))
        elif request.form["password"] == '':
            flash("Please enter your password", "info")
            return redirect(url_for("auth.register"))
        else:
            username = request.form["username"]
            email = request.form["email"]
            password = request.form["password"]
        
        # Check if a file is provided in the request
        if 'profile_image' in request.files:
            profile_image_file = request.files['profile_image']

            # Check if the file has an allowed extension (e.g., jpg, jpeg, png)
            if profile_image_file and allowed_file(profile_image_file.filename):
                # Save the file to a designated folder (you need to create this folder)
                filename = secure_filename(profile_image_file.filename)
                profile_image_file.save(os.path.join('static/uploads/users_image', filename))

                # Save the filename or path in the user database record
                profile_image_path = filename  # Assuming you have a 'profile_image' column in your User model

        # Store the data in the session
        flash(f"Register Successful!" , "info")

        #add new user to database
        usr = User(username=username, email=email, password=password, profile_image=profile_image_path)
        db.session.add(usr)
        db.session.commit()

        return redirect(url_for("auth.user"))
    else:
        return render_template('accounts/register.html')
    
# Add a function to check if the file has an allowed extension
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
################################################ login route #####################################################
@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        if request.form["email"] == '':
            flash("Please enter your email", "info")
            return redirect(url_for("auth.login"))
        elif request.form["password"] == '':
            flash("Please enter your password", "info")
            return redirect(url_for("auth.login"))
        else:
            email = request.form["email"]
            password = request.form["password"]
            #get the user form db where email == email and password == password
            usr = User.query.filter_by(email=email, password=password).first()
            if usr.status != 'active':
               flash(f"This account disabled for now ! , {email}", "info")
               return redirect(url_for("auth.login"))
            elif usr:
                session["username"] = usr.username
                session["email"] = usr.email
                session["password"] = usr.password
                flash(f"Login Successful! , {usr.username}", "info")
                return redirect(url_for("auth.user"))
            else:
                flash(f"Login Failed You Are Not Sign Up ! , {email}", "info")
                return redirect(url_for("auth.login"))
    else:
            if "username" in session:
                return redirect(url_for("auth.user"))
            return render_template('accounts/login.html')

################################################ route to delete user from database #################################
@auth.route("/delete", methods=["POST", "GET"])
def delete():
    if request.method == "POST":
        id = request.form["id"]
        usr = User.query.filter_by(_id=id).first()
        db.session.delete(usr)
        db.session.commit()
        flash(f"User Deleted Successfully!", "info")
        return redirect(url_for("auth.view"))
    else:
        return render_template('delete.html')
    
################################################ route to edit user in database ##################################
@auth.route("/edit", methods=["POST", "GET"])
def edit():
    if request.method == "POST":
        id = request.form["id"]
        usr = User.query.filter_by(_id=id).first()
        return render_template('accounts/edit.html',user = usr)
################################################ route to update user in database #################################
@auth.route("/update", methods=["POST", "GET"])
def update():
    if request.method == "POST":
        id = request.form["id"]

        usr = User.query.filter_by(_id=id).first()
        usr.username = request.form["username"]
        usr.email = request.form["email"]
        usr.password = request.form["password"]
        if request.form["role"] != '':
            usr.role = request.form["role"]

        if request.form["status"]:
            usr.status = request.form["status"]

        if usr.username == '':
            flash("Please enter your username to register", "info")
            return render_template('accounts/edit.html',user = usr)
        elif usr.email == '':
            flash("Please enter your email", "info")
            return render_template('accounts/edit.html',user = usr)
        elif usr.password == '':
            flash("Please enter your password", "info")
            return render_template('accounts/edit.html',user = usr)
        else:
            db.session.commit()
            flash(f"User Updated Successfully!", "info")
            return redirect(url_for("auth.view"))
    else:
        return render_template('accounts/edit.html',user = usr)
########################################### routeview to show all User in database ################################
@auth.route("/view")
def view():
    return render_template('accounts/view.html', values=User.query.all())
#################################################### logout route ##################################################
@auth.route("/logout")
def logout():
    flash(f"You have been logged out!", "info")
    session.pop("username", None)
    session.pop("email", None)
    session.pop("password", None)
    # flash(f"User Deleted Successfully ", "info")
    return redirect(url_for("auth.login"))
