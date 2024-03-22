from flask import Blueprint, render_template
from psycopg2 import Error

from .util import connect_db
from .util.basic_auth import auth

bp = Blueprint('edit', __name__)

def format_date(date_obj):
    return date_obj.strftime("%Y-%m-%d")

def int_hour(date_obj):
    return int(date_obj.strftime("%H"))

def int_minute(date_obj):
    return int(date_obj.strftime("%M"))

def get_data_by_id(id):
    conn = connect_db.connect_db()
    try:
        cursor = conn.cursor()
        query = f'SELECT id, start_datetime, end_datetime, location, comment, created_by FROM practices where id={id}'
        cursor.execute(query)
        data = cursor.fetchone()
        res = {
            'id': data[0],
            'date': format_date(data[1]),
            'start_time': data[1],
            'end_time': data[2],
            'location': data[3],
            'comment': data[4],
            'created_by': data[5]
        }
        return res

    except (Exception, Error) as error:
        print("error occurred in /list:", error)
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()

@bp.route('/edit/<int:id>')
@auth.login_required
def edit(id):
    data = get_data_by_id(id)
    return render_template('edit.html', data=data)
