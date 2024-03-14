from flask import Blueprint, render_template
from .util.basic_auth import auth

bp = Blueprint('register', __name__)

@bp.route('/', methods=['GET'])
@auth.login_required
def index():
    return render_template('register.html', active_menu='register')
