from flask import Blueprint, jsonify, request, abort
from dotenv import load_dotenv
import os
from psycopg2 import Error
from .util import connect_db, create_image, create_message
from .util.basic_auth import auth
from datetime import datetime, timedelta
from linebot import LineBotApi
from linebot.models import FlexSendMessage


def auth_token(f):
    def decorated_function(*args, **kwargs):
        load_dotenv()
        token = request.headers.get('Authorization', '').split(' ')[-1]
        if token != os.environ['CRON_TOKEN']:
            abort(401)
        return f(*args, **kwargs)
    return decorated_function

bp = Blueprint('announce', __name__)


@bp.route('/announce')
@auth_token
def announce():
    load_dotenv()
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    HIKINA_LINE_ID = os.environ['HIKINA_GROUP_ID_2024']
    line_bot_api = LineBotApi(ACCESS_TOKEN)

    def post_to_line(alt_title, title, content, img_name):
        payload = create_message.create_message(alt_title, title, content, img_name)
        container_obj = FlexSendMessage.new_from_json_dict(payload)
        line_bot_api.push_message(
            HIKINA_LINE_ID,
            messages=container_obj
        )

    today = datetime.now().date()
    tomorrow = today + timedelta(days=2) # UTC22:00から見た、JSTの翌日を取りたいので、days=2
    two_days_after = today + timedelta(days=3)
    get_practice_query = f'''
        SELECT id, start_datetime, end_datetime, location, comment, created_by FROM practices
        WHERE '{tomorrow}' <= start_datetime AND start_datetime < '{two_days_after}' AND NOT has_announced;
    '''
    announce_query = '''
        UPDATE practices
        SET has_announced = TRUE
        WHERE id = %s;
    '''

    conn = connect_db.connect_db()
    try:
        sent = 0
        while True:
            cursor = conn.cursor()
            cursor.execute(get_practice_query)
            data = cursor.fetchone()
            if data == None:
                break
            res = {
                'id': data[0],
                'start_datetime': data[1],
                'end_datetime': data[2],
                'location': data[3],
                'comment': data[4],
                'created_by': data[5]
            }
            cursor.execute(announce_query, (res['id'], ))
            alt_title = '練習会 参加調査'
            title = '【参加調査 by ' + res['created_by'] + ' 】'
            img_name = create_image.create_image(res['id'], res['start_datetime'], res['end_datetime'], res['location'])
            post_to_line(alt_title, title, res['comment'], img_name)
            sent += 1
            conn.commit()
        data = {'message': 'success', 'sent': sent}
        return jsonify(data), 200


    except (Exception, Error) as error:
        print("error occurred in /announce:", error)
        data = {'message': 'failed'}
        return jsonify(data), 503

    finally:
        if conn:
            cursor.close()
            conn.close()
