from flask import Blueprint, render_template

bp = Blueprint('register', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('register.html', active_menu='register')