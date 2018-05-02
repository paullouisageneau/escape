
const vm = new Vue({
	delimiters:['${', '}'],	// by default, it's {{ }}, which would conflicts with Flask Jinja templates
	el: '#console',			// the vue instance controls the element whose id is "control"
	data: {
		startTime: 0,		// timestamp at which the chrono was started
		elapsed: 0,			// seconds elapsed since startTime
		chrono: '',			// the chrono as displayed (HH:MM:SS)
		inputClue: '',		// the clue input from the user
		clues: [],			// the sent clues
		enabled: []			// the indexes of enabled toggles
	},
	mounted: function() {
		// Initialize chrono
		fetch('/api/chrono').then((response) => {
			return response.json();
		}).then((chrono) => {
			if(chrono.start) {
				this.startTime = chrono.start;
			}
		});
		
		// Initialize clues
		fetch('/api/clues').then((response) => {
			return response.json();
		}).then((array) => {
			this.clues = array.map(c => c.text);
		});
		
		// Initialize toggles
		fetch('/api/toggles').then((response) => {
			return response.json();
		}).then((array) => {
			// Initialize enabled with the indexes of the enabled toggles
			this.enabled = array.map((t, i) => t.value ? i.toString() : null).filter(i => i)
			
			// Now watch enabled for changes and post them
			this.$watch('enabled', function(array, oldArray) {
				function doPost(i, value) {
					const data = {
						value,
					}
					fetch(`/api/toggles/${i}`, {
						method: 'POST',
						body: JSON.stringify(data),
						headers: {
							'Content-Type': 'application/json'
						}
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
			this.startTime = time();
		},
		trigger: function(i) {
			fetch(`/api/triggers/${i}`, {
				method: 'POST',
			});
		},
		update: function() {
			// The chrono must be updated each second
			if(this.startTime > 0) {
				this.elapsed = Math.max(time() - this.startTime, 0);
				this.chrono = formatTime(this.elapsed);
			}
		},
		sendClue: function() {
			if(!this.inputClue) {
				alert("Entrez d'abord un indice.");
				return;
			}
			const data = {
				text: this.inputClue
			};
			fetch('/api/clues', {
				method: 'POST',
				body: JSON.stringify(data),
				headers: {
					'Content-Type': 'application/json'
				}
			}).then((response) => {
				return response.json();
			}).then((clue) => {
				this.clues.push(clue.text);
			});
			this.inputClue = '';
		},
		reset: function() {
			if(confirm("Voulez-vous vraiment réinitialiser la salle ?")) {
				fetch('/api/reset', {
					method: 'POST',
				}).then(() => {
					location.reload();
				});
			}
		},
	},
	watch: {
		startTime: function(value, oldValue) {
			if (value > time()) {
				this.startTime = time();
				return;
			}
			const data = {
				start: this.startTime,
			};
			fetch('/api/chrono', {
				method: 'POST',
				body: JSON.stringify(data),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			this.update();
		}
	}
});
