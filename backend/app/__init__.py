import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

app=Flask(__name__)
app.config.from_object(Config)

app.config["SECRET_KEY"] = "your-secret-key"

db=SQLAlchemy(app)
migrate=Migrate(app,db)

CORS(app, supports_credentials=True, origins=["http://127.0.0.1:5173"])

from app import routes, models
from app.routes import init_routes
init_routes(app)