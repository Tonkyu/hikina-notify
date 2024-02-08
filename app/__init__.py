from flask import Flask

from .form import bp as form_bp
from .get_image import bp as get_image_bp
from util import connect_db

def create_app():
    app = Flask(__name__)

    app.register_blueprint(form_bp)
    app.register_blueprint(get_image_bp)

    connect_db.connect_db()

    return app
