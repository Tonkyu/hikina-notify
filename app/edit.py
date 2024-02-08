from flask import Blueprint, render_template
from psycopg2 import Error

from util import connect_db

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
        query = f'SELECT * FROM practices where id={id}'
        cursor.execute(query)
        data = cursor.fetchone()
        res = (
            data[0],
            format_date(data[1]),
            int_hour(data[1]),
            int_minute(data[1]),
            int_hour(data[2]),
            int_minute(data[2]),
            data[3]
            )
        return res

    except (Exception, Error) as error:
        print("error occurred in /list:", error)
        return None

    finally:
        if conn:
            cursor.close()
            conn.close()

@bp.route('/edit/<int:id>')
def edit(id):
    data = get_data_by_id(id)
    return render_template('edit.html', data=data)
