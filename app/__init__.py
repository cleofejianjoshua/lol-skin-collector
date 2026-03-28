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

CORS(app, supports_credentials=True)

from app import routes, models
from app.routes import init_routes
init_routes(app)