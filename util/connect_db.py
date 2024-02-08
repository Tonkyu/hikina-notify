import psycopg2
from dotenv import load_dotenv
import os


def connect_db():
    load_dotenv()
    DATABASE_URL = os.environ['DATABASE_URL']
    IS_DEBUG = os.environ['IS_DEBUG']

    if IS_DEBUG:
        conn = psycopg2.connect(DATABASE_URL)
    else :
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn