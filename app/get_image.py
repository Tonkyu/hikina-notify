from flask import Blueprint, send_file, request
import os

import util.create_image as create_image

bp = Blueprint('get_image', __name__)

@bp.route('/get_image', methods=['POST'])
def get_image():
	data = request.json

	image_path = create_image(data)
	if not os.path.exists(image_path):
		return "Image not found", 404

	return send_file(image_path, mimetype='image/jpg')