from config import Config
from flask import (Flask, Response, jsonify, redirect, render_template, request,
                   send_from_directory, url_for, send_file, make_response, session, url_for, flash, Blueprint)
import os
from app import app
from flask import redirect, render_template, url_for

app = Blueprint('app', __name__)

base_dir = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=["GET"])
def default():
    return redirect(url_for('app.home'))

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html", title="Conversation Analyser", dark_mode=0)

@app.route("/analyse", methods=["GET", "POST"])
def test():

    return render_template("analyse.html", title="Conversation Analyser", dark_mode=0)