from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import os
import dotenv

dotenv.load_dotenv()
auth = HTTPBasicAuth()

users = {
    os.environ.get("BASIC_USERNAME"): generate_password_hash(os.environ.get("BASIC_PASSWORD"))
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False
