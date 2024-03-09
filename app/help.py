from flask import Blueprint, render_template

bp = Blueprint('help', __name__)

@bp.route('/help/', methods=['GET'])
def help():
    return render_template('help.html')
