from flask import Blueprint, request, jsonify, redirect, url_for
from psycopg2 import Error
from util import connect_db
from datetime import datetime

bp = Blueprint('update', __name__)

@bp.route('/update/<int:id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        date = request.form['date']
        start_hour = request.form['start_hour']
        start_minute = request.form['start_minute']
        end_hour = request.form['end_hour']
        end_minute = request.form['end_minute']
        location = request.form['location']

        start_datetime = datetime.strptime(f"{date} {start_hour}:{start_minute}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_hour}:{end_minute}", "%Y-%m-%d %H:%M")

        update_query = '''
            UPDATE practices
            SET start_datetime=%s, end_datetime=%s, location=%s
            WHERE id=%s;
        '''

        conn = connect_db.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute(update_query, (start_datetime, end_datetime, location, id))
            conn.commit()
            return redirect(url_for('list.list'))

        except (Exception, Error) as error:
            print("error occurred in /update(POST):", error)
            data = {'message': 'failed'}
            return jsonify(data), 503

        finally:
            if conn:
                cursor.close()
                conn.close()
