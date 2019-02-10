
import sys
import os
import json

# Make threading cooperative
from gevent import monkey
monkey.patch_all()

from flask import Flask, request, Response, abort, render_template, send_from_directory, jsonify, url_for

from .room import Room

# ----- App initialization -----

# Create the Flask app
app = Flask(__name__, static_url_path='/static')

# Import config from config.py file
app.config.from_object('config')

# Import room configuration
room = Room(app.config['ROOM_NAME'])

# ----- Routes definition -----

@app.route('/media/<path:filename>')
def media_file(filename):
	return send_from_directory(app.config['MEDIA_PATH'], filename, conditional=True)

@app.route('/', methods=['GET'])
def home():
	return render_template('control.html', room=room)

@app.route('/display', methods=['GET'])
def display():
	return render_template('display.html', room=room)

@app.route('/camera', methods=['GET'])
def camera():
	return render_template('camera.html', room=room)

@app.route('/api/camera/<int:index>', methods=['POST'])
def camera_controller(index):
	if index not in range(len(room.cameras)):
		abort(404)
	camera = room.cameras[index]
	if not camera.controller:
		abort(404)
	data = request.get_json()
	action = data.get('action', 'stop')
	if not camera.controller.command(action):
		abort(500)
	return Response('', 204)

@app.route('/api/reset', methods=['POST'])
def api_reset():
	room.reset()
	return Response('', 204)

@app.route('/api/chrono', methods=['GET', 'POST'])
def api_chrono():
	if request.method == 'POST':
		data = request.get_json()
		start_time = data['start']
		stop_time = data['stop']
		room.set_chrono(start_time, stop_time)
	return jsonify({ 'start': room.start_time, 'stop': room.stop_time })

@app.route('/api/clues', methods=['GET', 'POST'])
def api_clues():
	if request.method == 'POST':
		data = request.get_json()
		clue = data['text']
		if clue:
			room.set_clue(clue)
			room.notify()
			return jsonify({ 'text': clue, 'index': len(room.clues)-1 })
		else:
			room.set_clue('')
			return Response('', 204)
	return jsonify([{ 'text': c } for c in room.clues])

@app.route('/api/clues/current', methods=['GET'])
def api_last_clue():
	if room.current_clue:
		return jsonify({ 'text': room.current_clue, 'index': len(room.clues)-1 })
	else:
		return jsonify({ 'text': '', 'index': -1 })

@app.route('/api/clues/<int:index>', methods=['GET'])
def api_clue(index):
	if index >= len(room.clues):
		abort(404)
	return jsonify({ 'text': room.clues[index] })

@app.route('/api/messages', methods=['GET', 'POST'])
def api_messages():
	if request.method == 'POST':
		message = request.get_json()
		room.handle_message(message)
		return jsonify(message)
	return jsonify(room.messages)

@app.route('/api/messages/<int:index>', methods=['GET'])
def api_message(index):
	if index >= len(room.messages):
		abort(404)
	return jsonify(room.messages[index])

@app.route('/api/toggles', methods=['GET'])
def api_toggles():
	return jsonify([t.to_dict() for t in room.toggles])

@app.route('/api/toggles/<int:index>', methods=['GET', 'POST'])
def api_toggle(index):
	if index >= len(room.toggles):
		abort(404)
	toggle = room.toggles[index]
	if request.method == 'POST':
		data = request.get_json()
		toggle.value = bool(data['value'])
	return jsonify(toggle.to_dict())

@app.route('/api/triggers', methods=['GET'])
def api_triggers():
	return jsonify([t.to_dict() for t in room.triggers])

@app.route('/api/triggers/<int:index>', methods=['GET', 'POST'])
def api_trigger(index):
	if index >= len(room.triggers):
		abort(404)
	trigger = room.triggers[index]
	triggered = False
	if request.method == 'POST':
		triggered = trigger.pull()
	response = trigger.to_dict()
	response['triggered'] = triggered
	return jsonify(response)

@app.route('/api/events', methods=['GET'])
def api_events():
	event_stream = room.subscribe()
	resp = Response(event_stream, mimetype="text/event-stream")
	resp.headers['Cache-Control'] = 'no-cache'
	resp.headers['X-Accel-Buffering'] = 'no'
	return resp

# Import main to expose it outside
from .__main__ import main

