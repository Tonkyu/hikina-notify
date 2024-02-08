from flask import Blueprint, render_template, request, jsonify
from psycopg2 import Error
from util import connect_db
from datetime import datetime

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

        start_datetime = datetime.strptime(f"{date} {start_hour}:{start_minute}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_hour}:{end_minute}", "%Y-%m-%d %H:%M")

        insert_query = '''
            INSERT INTO practices (start_datetime, end_datetime, location)
            VALUES (%s, %s, %s);
        '''

        conn = connect_db.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute(insert_query, (start_datetime, end_datetime, location))
            conn.commit()

            data = {'message': 'success'}
            return jsonify(data), 200

        except (Exception, Error) as error:
            print("error occurred in /submit(POST):", error)
            data = {'message': 'failed'}
            return jsonify(data), 503

        finally:
            if conn:
                cursor.close()
                conn.close()
                print("closed connection")
