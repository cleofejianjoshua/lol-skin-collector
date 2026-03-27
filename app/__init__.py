from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

app=Flask(__name__)
app.config.from_object(Config)

db=SQLAlchemy(app)
migrate=Migrate(app,db)

CORS(app, supports_credentials=True)

from app import routes, models
from app.routes import register_routes
register_routes(app)