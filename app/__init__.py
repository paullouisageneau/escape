
import sys
import os

from flask import Flask, request, Response, abort, render_template, jsonify, url_for
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
    return render_template('control.html', room=room)

@app.route('/display', methods=['GET'])
def display():
    return render_template('display.html', room=room)

@app.route('/api/cameras', methods=['GET'])
def cameras():
	return jsonify(room.cameras)

@app.route('/api/cameras/<int:index>', methods=['GET'])
def camera(index):
	if index >= len(room.cameras):
		abort(404)
	return jsonify(room.cameras[index])

@app.route('/api/toggles', methods=['GET'])
def toggles():
	return jsonify([t.to_dict() for t in room.toggles])

@app.route('/api/toggles/<int:index>', methods=['GET', 'POST'])
def toggle(index):
	if index >= len(room.toggles):
		abort(404)
	toggle = room.toggles[index];
	if request.method == 'POST':
		data = request.get_json()
		toggle.value = bool(data['value'])
	return jsonify(toggle.to_dict())

