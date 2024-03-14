from flask import Flask

from .register import bp as register_bp
from .list import bp as list_bp
from .submit import bp as submit_bp
from .edit import bp as edit_bp
from .delete import bp as delete_bp
from .update import bp as update_bp
from .announce import bp as announce_bp
from .help import bp as help_bp
from .util import connect_db

def create_app():
    app = Flask(__name__)
    app.static_folder = '../static'

    app.register_blueprint(register_bp)
    app.register_blueprint(list_bp)
    app.register_blueprint(submit_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(update_bp)
    app.register_blueprint(announce_bp)
    app.register_blueprint(help_bp)

    connect_db.connect_db()
    return app
