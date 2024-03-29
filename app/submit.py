from flask import Blueprint, request, jsonify, redirect, url_for
from psycopg2 import Error
from datetime import datetime
from .util import connect_db
from .util.basic_auth import auth


bp = Blueprint('submit', __name__)

@bp.route('/submit', methods=['POST'])
@auth.login_required
def submit():
    if request.method == 'POST':
        date = request.form['date']
        start_hour = request.form['start_hour']
        start_minute = request.form['start_minute']
        end_hour = request.form['end_hour']
        end_minute = request.form['end_minute']
        location = request.form['location']
        comment = request.form['comment']
        created_by = request.form['created_by']

        start_datetime = datetime.strptime(f"{date} {start_hour}:{start_minute}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.strptime(f"{date} {end_hour}:{end_minute}", "%Y-%m-%d %H:%M")

        insert_query = '''
            INSERT INTO practices (start_datetime, end_datetime, location, comment, created_by)
            VALUES (%s, %s, %s, %s, %s);
        '''

        conn = connect_db.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute(insert_query, (start_datetime, end_datetime, location, comment, created_by))
            conn.commit()
            return redirect(url_for('list.list'))

        except (Exception, Error) as error:
            print("error occurred in /submit(POST):", error)
            data = {'message': 'failed'}
            return jsonify(data), 503

        finally:
            if conn:
                cursor.close()
                conn.close()
