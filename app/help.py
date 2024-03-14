from flask import Blueprint, render_template
from util.basic_auth import auth

bp = Blueprint('help', __name__)

@bp.route('/help/', methods=['GET'])
@auth.login_required
def help():
    return render_template('help.html')
