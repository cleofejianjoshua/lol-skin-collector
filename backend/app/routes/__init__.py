from .auth import auth
from .main import main
from .api import api

def init_routes(app):
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(api)