
import sys
import os
import time
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

# If chrono was started, startTime contains the corresponding timestamp
startTime = 0

# If chrono was stopped, stopTime contains the corresponding timestamp
stopTime = 0

# List of the sent clues
clues = []

# Current displayed clue
currentClue = ''

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
	if not index in range(len(room.cameras)):
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
	global startTime, stopTime, clues, currentClue
	startTime = 0
	stopTime = 0
	clues = []
	currentClue = ''
	room.reset()
	return Response('', 204)

@app.route('/api/chrono', methods=['GET', 'POST'])
def api_chrono():
	global startTime, stopTime
	if request.method == 'POST':
		data = request.get_json()
		startTime = data['start']
		stopTime = data['stop']
		clue = ''
		room.events.publish('chrono', json.dumps({ 'start': startTime, 'stop': stopTime }))
	return jsonify({ 'start': startTime, 'stop': stopTime })

@app.route('/api/clues', methods=['GET', 'POST'])
def api_clues():
	global clues, currentClue
	if request.method == 'POST':
		data = request.get_json()
		clue = data['text']
		if clue:
			clues.append(clue)
			currentClue = clue
			room.events.publish('clue', json.dumps({ 'text': clue }))
			room.notify()
			return jsonify({ 'text': clue, 'index': len(clues)-1 })
		else:
			# Posting an empty clue allows to hide the displayed one
			currentClue = ''
			room.events.publish('clue', json.dumps({ 'text': '' }))
			return Response('', 204)
	return jsonify([{ 'text': c } for c in clues])

@app.route('/api/clues/current', methods=['GET'])
def api_last_clue():
	global clues, currentClue
	if currentClue:
		return jsonify({ 'text': currentClue, 'index': len(clues)-1 })
	else:
		return jsonify({ 'text': '', 'index': -1 })

@app.route('/api/clues/<int:index>', methods=['GET'])
def api_clue(index):
	if index >= len(clues):
		abort(404)
	return jsonify({ 'text': clues[index] })

@app.route('/api/toggles', methods=['GET'])
def api_toggles():
	return jsonify([t.to_dict() for t in room.toggles])

@app.route('/api/toggles/<int:index>', methods=['GET', 'POST'])
def api_toggle(index):
	if index >= len(room.toggles):
		abort(404)
	toggle = room.toggles[index];
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
	response = trigger.to_dict()
	response['triggered'] = False
	if request.method == 'POST':
		response['triggered'] = trigger.pull()
	return jsonify(response)

@app.route('/api/events', methods=['GET'])
def api_events():
	global startTime, stopTime
	event_stream = room.events.subscribe()
	room.events.publish('chrono', json.dumps({ 'start': startTime, 'stop': stopTime }))
	room.events.publish('clue', json.dumps({ 'text': currentClue }))
	resp = Response(event_stream, mimetype="text/event-stream")
	resp.headers['Cache-Control'] = 'no-cache'
	resp.headers['X-Accel-Buffering'] = 'no'
	return resp

