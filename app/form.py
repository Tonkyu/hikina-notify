from flask import Blueprint, render_template, request, jsonify

bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@bp.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        date = request.form['date']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        location = request.form['location']

        data = {'message': 'success'}
        return jsonify(data), 200