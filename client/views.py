from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import Task
from . import db
import json
from cloudipsp import Api, Checkout

views = Blueprint("views", __name__)

@views.route("/", methods=["GET", "POST"])
@login_required
def home():
  if request.method == "POST":
    #action = request.form.get("action")
    #task_value = request.form.get("task")
    #print(action, task_value)
    
    action, task_value = request.form

    if action == "remove":
      task = Task.query.get(int(task_value))
      db.session.delete(task)
      db.session.commit()
    elif action == "add":
      task = Task(value=task_value, user_id=current_user.id)
      db.session.add(task)
      db.session.commit()

  return render_template("home.html", user=current_user)

@views.route("/remove-task", methods=["POST"])
def remove_task():
  id = json.loads(request.data)["id"]
  task = Task.query.get(int(id))
  db.session.delete(task)
  db.session.commit()
  return { "ok": True }

@views.route("/remove-task/<string:id>", methods=["POST"])
def remove_task_by_id(id):
  task = Task.query.get(int(id))
  db.session.delete(task)
  db.session.commit()
  return { "ok": True }

@views.route("/buy", methods=["GET"])
def buy_item():
  price = 146
  api = Api(merchant_id=1396424, secret_key="test")
  checkout = Checkout(api=api)
  data = {
    "currency": "UAH",
    "amount": price * 100
  }
  url = checkout.url(data).get('checkout_url')
  return redirect(url)
