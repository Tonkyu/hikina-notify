from flask import Blueprint, jsonify
from dotenv import load_dotenv
import os
from psycopg2 import Error
from util import connect_db, create_image, create_message
from util.basic_auth import auth
from datetime import datetime, timedelta
from linebot import LineBotApi
from linebot.models import FlexSendMessage

bp = Blueprint('announce', __name__)


@bp.route('/announce', methods=['POST'])
@auth.login_required
def announce():
    load_dotenv()
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    HIKINA_LINE_ID = os.environ['TONQ_GROUP_ID']
    line_bot_api = LineBotApi(ACCESS_TOKEN)

    def post_to_line(alt_title, title, content, img_name):
        payload = create_message.create_message(alt_title, title, content, img_name)
        container_obj = FlexSendMessage.new_from_json_dict(payload)
        line_bot_api.push_message(
            HIKINA_LINE_ID,
            messages=container_obj
        )

    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)
    two_days_after = today + timedelta(days=2)
    get_practice_query = f'''
        SELECT * FROM practices
        WHERE '{tomorrow}' <= start_datetime AND start_datetime < '{two_days_after}' AND NOT has_announced;
    '''
    announce_query = '''
        UPDATE practices
        SET has_announced = TRUE
        WHERE id = %s;
    '''

    conn = connect_db.connect_db()
    try:
        while True:
            cursor = conn.cursor()
            cursor.execute(get_practice_query)
            res = cursor.fetchone()
            if res == None:
                break
            id = res[0]
            cursor.execute(announce_query, (id,))
            conn.commit()
            alt_title = '練習会 参加調査'
            title = '【練習会 参加調査】'
            content = '明日は練習会です。\n参加できる方はこのメッセージに\nリアクションをお願いします！'
            img_name = create_image.create_image(res)
            post_to_line(alt_title, title, content, img_name)
        data = {'message': 'success'}
        return jsonify(data), 200


    except (Exception, Error) as error:
        print("error occurred in /announce(POST):", error)
        data = {'message': 'failed'}
        return jsonify(data), 503

    finally:
        if conn:
            cursor.close()
            conn.close()
