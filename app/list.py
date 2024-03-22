from flask import Blueprint, render_template, request
from psycopg2 import Error
from datetime import datetime

from .util import connect_db
from .util.basic_auth import auth

bp = Blueprint('list', __name__)

def format_date(date_obj):
    return date_obj.strftime("%m/%d")

def format_time(date_obj):
    return date_obj.strftime("%H:%M")

def get_data(show_past_bool):
    conn = connect_db.connect_db()
    try:
        cursor = conn.cursor()
        today = datetime.now().date()
        query = f'''
            SELECT id, start_datetime, end_datetime, location, comment, created_by, has_announced FROM practices
            ORDER BY start_datetime;
        ''' if show_past_bool else f'''
            SELECT id, start_datetime, end_datetime, location, comment, created_by, has_announced FROM practices
            WHERE start_datetime >= '{today}'
            ORDER BY start_datetime;
        '''
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        res = [{
            'id': element[0],
            'date': format_date(element[1]),
            'start_time': format_time(element[1]),
            'end_time': format_time(element[2]),
            'location': element[3],
            'comment': element[4],
            'created_by': element[5],
            'has_announced': element[6]
        } for element in data]
        return res

    except (Exception, Error) as error:
        print("error occurred in /list:", error)
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()

@bp.route('/list/')
@auth.login_required
def list():
    show_past = request.args.get('show_past', default='false')
    show_past_bool = show_past != 'false'
    data = get_data(show_past_bool)
    return render_template('list.html', data=data, active_menu='list', show_past=show_past)
