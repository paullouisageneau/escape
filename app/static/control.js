
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#control',			// the vue instance controls the element whose id is "control"
	data: {
		startTime: 0,	// timestamp at which the chrono was started
		stopTime: 0,	// timestamp at which the chrono was stopped
		elapsed: 0,		// seconds elapsed since startTime
		chrono: '00:00:00',	// the chrono as displayed (HH:MM:SS)
		inputClue: '',		// the clue input from the user
		clues: [],			// all the sent clues
		currentClueIndex: -1,	// index of the current clue
		show: false,	// last clue is visible
		enabled: []		// the indexes of enabled toggles
	},
	mounted: function() {
		// Initialize chrono
		getJson('/api/chrono', (chrono) => {
			this.startTime = chrono.start;
			this.stopTime = chrono.stop;
		});

		// Initialize clues history
		getJson('/api/clues', (array) => {
			this.clues = array.map(c => c.text);
		});
		
		// Initialize current clue index
		getJson('/api/clues/current', (clue) => {
			this.currentClueIndex = clue.index;
		});

		// Initialize toggles
		getJson('/api/toggles', (array) => {
			// Initialize enabled with the indexes of the enabled toggles
			this.enabled = array.map((t, i) => t.value ? i.toString() : null).filter(i => i)
			
			// Now watch enabled for changes and post them
			this.$watch('enabled', function(array, oldArray) {
				function doPost(i, value) {
					postJson(`/api/toggles/${i}`, {
						value
					});
				};
				array.filter(i => !oldArray.includes(i)).forEach(i => doPost(i, true));
				oldArray.filter(i => !array.includes(i)).forEach(i => doPost(i, false));
			});
		});
		
		// Setup update callback every second
		setInterval(this.update, 1000);
	},
	methods: {
		start: function() {
			// stopTime set to zero means the chronometer is running
			this.startTime = this.startTime + (time() - this.stopTime);
			this.stopTime = 0;
		},
		stop: function() {
			// stopTime set to nonzero value means the chronometer is stopped at stopTime
			this.stopTime = time();
		},
		trigger: function(i) {
			postJson(`/api/triggers/${i}`, {}, (trigger) => {
				// The name of the trigger can have changed
				if(trigger.name) {
					const input = document.getElementById(`trigger-${i}`);
					input.value = trigger.name;
				}
			});
		},
		update: function() {
			// The chrono must be updated each second
			if(this.startTime > 0) {
				// refTime is the reference to compute elapsed time
				const refTime = this.stopTime > 0 ? this.stopTime : time();
				
				// elapsed is the time since refTime
				this.elapsed = Math.max(refTime - this.startTime, this.elapsed);
			}
			else {
				this.elapsed = 0;
			}
			
			this.chrono = formatTime(this.elapsed);
		},
		syncTime: function() {
			postJson('/api/chrono', {
				start: this.startTime,
				stop: this.stopTime
			});
		},
		sendClue: function(text) {
			if(!text) {
				if(!this.inputClue) {
					alert("Entrez d'abord un indice.");
					return;
				}
				text = this.inputClue;
				this.inputClue = '';
			}
			postJson('/api/clues', {
				text: text
			}, (clue) => {
				this.clues.push(clue.text);
				this.currentClueIndex = this.clues.length-1;
				setTimeout(() => {
					const scroll = this.$el.querySelector("#clues .scroll");
					scroll.scrollTop = scroll.scrollHeight;
				}, 0);
			});
		},
		hideClue: function() {
			this.currentClueIndex = -1;
			postJson('/api/clues', {
				text: ''
			}, (clue) => {
				this.show = false;
			});
		},
		reset: function() {
			if(confirm("Voulez-vous vraiment réinitialiser la salle ?")) {
				postJson('/api/reset', {}, () => {
					location.reload();
				});
			}
		}
	},
	watch: {
		startTime: function(value, oldValue) {
			if(value > time()) {
				this.startTime = time();
				return;
			}
			this.elapsed = 0;	// Allow the chrono to decrease
			this.syncTime();
			this.update();
		},
		stopTime: function(value, oldValue) {
			if(!value) return;
			this.syncTime();
			this.update();
		}
	}
});
