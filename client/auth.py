from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    name = request.form.get("name")
    password = request.form.get("password")
    user = User.query.filter_by(name=name).first()
    if user:
      if check_password_hash(user.password, password):
        flash("Logged in!", category="success")
        login_user(user, remember=True)
        return redirect(url_for("views.home"))
      else:
        flash("Wrong password", category="error")
    else:
      flash("Name doesn't exists", category="error")
    
  return render_template("login.html", customValue="🥒", user=current_user)

@auth.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    name = request.form.get("name")
    password = request.form.get("password")
    user = User.query.filter_by(name=name).first()
    if user:
      flash("User already exists", category="error")
    else:
      new_user = User(name=name, password=generate_password_hash(password, method="sha256"))
      db.session.add(new_user)
      db.session.commit()
      flash("User created!", category="success")
      login_user(new_user, remember=True)
      return redirect(url_for("views.home"))
    
  return render_template("register.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for("auth.login"))
