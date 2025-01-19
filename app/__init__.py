from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config.from_object(Config)

from .routes import app as app_blueprint
app.register_blueprint(app_blueprint)
