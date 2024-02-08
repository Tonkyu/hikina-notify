from flask import Flask

from .register import bp as register_bp
from .get_image import bp as get_image_bp
from .list import bp as list_bp
from .submit import bp as submit_bp
from .edit import bp as edit_bp
from .delete import bp as delete_bp
from .update import bp as update_bp
from util import connect_db

def create_app():
    app = Flask(__name__)

    app.register_blueprint(register_bp)
    app.register_blueprint(get_image_bp)
    app.register_blueprint(list_bp)
    app.register_blueprint(submit_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(update_bp)

    connect_db.connect_db()

    return app
