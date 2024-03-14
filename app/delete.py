from flask import Blueprint, request, jsonify, redirect, url_for
from psycopg2 import Error
from .util import connect_db
from .util.basic_auth import auth

bp = Blueprint('delete', __name__)

@bp.route('/delete/<int:id>', methods=['POST'])
@auth.login_required
def delete(id):
    if request.method == 'POST':
        delete_query = f'''
            DELETE FROM practices
            WHERE id={id};
        '''
        conn = connect_db.connect_db()

        try:
            cursor = conn.cursor()
            cursor.execute(delete_query)
            conn.commit()
            res = redirect(url_for('list.list'))

        except (Exception, Error) as error:
            print("error occurred in /delete(POST):", error)
            data = {'message': 'failed'}
            res = jsonify(data), 503

        finally:
            if conn:
                cursor.close()
                conn.close()
            return res
