
import sys
import os
import time
import json

from flask import Flask, request, Response, abort, render_template, jsonify, url_for

from .room import Room

# ----- App initialization -----

# Create the Flask app
app = Flask(__name__)

# Import config from config.py file
app.config.from_object('config')

# Import room configuration
room = Room(app.config['ROOM_NAME'])

# If chrono was started, startTime contains the corresponding timestamp
startTime = 0

# List of the sent clues
clues = []

# ----- Routes definition -----

@app.route('/', methods=['GET'])
def home():
    return render_template('control.html', room=room)

@app.route('/display', methods=['GET'])
def display():
	return render_template('display.html', room=room)

@app.route('/api/reset', methods=['POST'])
def api_reset():
	global startTime
	global clues
	startTime = 0
	clues = []
	for toggle in room.toggles:
		toggle.reset()
	room.events.publish('reset', json.dumps({}))
	return Response('', 204)

@app.route('/api/chrono', methods=['GET', 'POST'])
def api_chrono():
	global startTime
	if request.method == 'POST':
		data = request.get_json()
		startTime = data['start']
		clue = ''
		room.events.publish('chrono', json.dumps({ 'start': startTime }))
	return jsonify({ 'start': startTime })

@app.route('/api/clues', methods=['GET', 'POST'])
def api_clues():
	global clues
	if request.method == 'POST':
		data = request.get_json()
		clue = data['text']
		clues.append(clue)
		room.events.publish('clue', json.dumps({ 'text': clue }))
		return jsonify({ 'text': clue, 'index': len(clues)-1 })
	return jsonify([{ 'text': c } for c in clues])

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
	global startTime
	event_stream = room.events.subscribe()
	print(startTime)
	room.events.publish('chrono', json.dumps({ 'start': startTime }))
	return Response(event_stream, mimetype="text/event-stream")

