from flask import Flask, request, send_file
import os

app = Flask(__name__)

IMAGE_FILE_PATH = 'hoge.png'

@app.route('/get_image', methods=['POST'])
def get_image():
	data = request.json

	return send_file(IMAGE_FILE_PATH, mimetype='image/png')

if __name__ == '__main__':
	app.run(debug=True)
