
import sys
import os

from flask import Flask, request, Response, render_template, url_for
from .room import Room

# ----- App initialization -----

# Create the Flask app
app = Flask(__name__)

# Import config from config.py file
app.config.from_object('config')

# Import room configuration
room = Room(app.config['ROOM_NAME'])

# ----- Routes definition -----

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html', room=room)

@app.route('/test', methods=['POST'])
def test():
	data = request.get_json()
	return Response('', 204)
