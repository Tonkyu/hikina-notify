from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@bp.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        date = request.form['date']
        start_hour = request.form['start_hour']
        start_minute = request.form['start_minute']
        end_hour = request.form['end_hour']
        end_minute = request.form['end_minute']
        location = request.form['location']

        data = {'message': 'success'}
        return jsonify(data), 200