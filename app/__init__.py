
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

# If chrono was stopped, stopTime contains the corresponding timestamp
stopTime = 0

# List of the sent clues
clues = []

# Last clue not visible
hideClue = True

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
	global stopTime
	global clues
	global hideClue
	startTime = 0
	stopTime = 0
	clues = []
	hideClue = True
	for toggle in room.toggles:
		toggle.reset()
	room.events.publish('reset', json.dumps({}))
	return Response('', 204)

@app.route('/api/chrono', methods=['GET', 'POST'])
def api_chrono():
	global startTime
	global stopTime
	if request.method == 'POST':
		data = request.get_json()
		startTime = data['start']
		stopTime = data['stop']
		clue = ''
		room.events.publish('chrono', { 'start': startTime, 'stop': stopTime })	
	return jsonify({ 'start': startTime, 'stop': stopTime })

@app.route('/api/clues', methods=['GET', 'POST'])
def api_clues():
	global clues
	global hideClue
	if request.method == 'POST':
		data = request.get_json()
		clue = data['text']
		clues.append(clue)
		hideClue = False
		room.events.publish('clue', json.dumps({ 'text': clue }))
		return jsonify({ 'text': clue, 'index': len(clues)-1, 'hide':hideClue })
	return jsonify([{ 'text': c } for c in clues])

@app.route('/api/clues/hide', methods=['GET', 'POST'])
def api_hide_clue():
	global clues
	global hideClue
	last_clue = ''
	if len(clues)>0: last_clue = clues[-1] 
	if request.method == 'POST':
		hideClue = True
		room.events.publish('hide clue', { 'hide': hideClue, 'text':last_clue })	
		return jsonify({ 'hide': hideClue })
	return jsonify({ 'hide': hideClue, 'text':last_clue })

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

