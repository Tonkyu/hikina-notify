from flask import Blueprint, request, jsonify, redirect, url_for
from psycopg2 import Error
from util import connect_db
from datetime import datetime, timedelta

bp = Blueprint('announce', __name__)

@bp.route('/announce')
def announce():
    today = datetime.now().date()
    two_days_after = today + timedelta(days=2)
    announce_query = '''
        UPDATE practices
        SET has_announced = TRUE
        WHERE start_datetime < %s;
    '''

    conn = connect_db.connect_db()
    try:
        cursor = conn.cursor()
        cursor.execute(announce_query, (two_days_after))
        conn.commit()
        data = {'message': 'success'}
        return jsonify(data), 200


    except (Exception, Error) as error:
        print("error occurred in /update(POST):", error)
        data = {'message': 'failed'}
        return jsonify(data), 503

    finally:
        if conn:
            cursor.close()
            conn.close()