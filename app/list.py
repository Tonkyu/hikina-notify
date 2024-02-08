from flask import Blueprint, render_template
from psycopg2 import Error
from datetime import datetime

from util import connect_db

bp = Blueprint('list', __name__)

def format_date(date_obj):
    return date_obj.strftime("%m/%d")

def format_time(date_obj):
    return date_obj.strftime("%H:%M")

def get_data():
    conn = connect_db.connect_db()
    try:
        cursor = conn.cursor()
        query = 'SELECT * FROM practices ORDER BY start_datetime'
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        res = [(
            element[0],
            format_date(element[1]),
            format_time(element[1]),
            format_time(element[2]),
            element[3],
            element[5],
        ) for element in data]
        return res

    except (Exception, Error) as error:
        print("error occurred in /list:", error)
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()

@bp.route('/list')
def list():
    data = get_data()
    return render_template('list.html', data=data, active_menu='list')
