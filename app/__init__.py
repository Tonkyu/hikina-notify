from flask import Flask
import psycopg2
from psycopg2 import Error
import os

from .form import bp as form_bp
from .get_image import bp as get_image_bp

def connect_db():
    conn_params = {
        "host": os.environ.get("DB_HOST"),
        "dB": os.environ.get("DB_NAME"),
        "user": os.environ.get("DB_USER"),
        "password": os.environ.get("DB_PASSWORD"),
        "port": os.environ.get("DB_PORT")
}
    # テーブルを作成するSQLクエリ
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS example_table (
            id SERIAL PRIMARY KEY,
            column1 VARCHAR(255),
            column2 INTEGER
        );
    '''

    # connection = psycopg2.connect(**conn_params)
    # try:
    #     # PostgreSQLデータベースに接続
    #     cursor = connection.cursor()

    #     # テーブルを作成
    #     cursor.execute(create_table_query)
    #     connection.commit()
    #     print("テーブルが作成されました")

    # except (Exception, Error) as error:
    #     print("エラーが発生しました:", error)

    # finally:
    #     # 接続を閉じる
    #     if connection:
    #         cursor.close()
    #         connection.close()
    #         print("接続が閉じられました")

def create_app():
    app = Flask(__name__)

    app.register_blueprint(form_bp)
    app.register_blueprint(get_image_bp)

    connect_db()

    return app
