from .auth import auth
from .main import main
from .api import api
from .gacha import gacha

def init_routes(app):
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(api)
    app.register_blueprint(gacha)